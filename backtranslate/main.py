import sys
import json
from PySide6.QtWidgets import QApplication

from backtranslate.config import load_config
from backtranslate.database.connection import init_db, get_connection
from backtranslate.database.operations import (
    update_evaluation_status, get_subtitles_for_session,
)

from backtranslate.ui.main_window import MainWindow
from backtranslate.ui.learn_page import LearnPage
from backtranslate.ui.review_page import ReviewPage
from backtranslate.ui.expressions_page import ExpressionsPage
from backtranslate.ui.settings_page import SettingsPage

from backtranslate.ai.worker import EvaluationWorker, EvaluationThread


class App:
    def __init__(self):
        self.window = MainWindow()
        self.worker = None
        self.eval_thread = None
        self._setup_pages()
        self._setup_worker()

    def _setup_pages(self):
        self.learn_page = LearnPage()
        self.review_page = ReviewPage()
        self.expressions_page = ExpressionsPage()
        self.settings_page = SettingsPage()

        self.window.set_learn_page(self.learn_page)
        self.window.set_review_page(self.review_page)
        self.window.set_expressions_page(self.expressions_page)
        self.window.set_settings_page(self.settings_page)

        self.learn_page.translation_submitted.connect(self._on_translation_submitted)
        self.review_page.redo_submitted.connect(self._on_redo_submitted)
        self.review_page.retry_requested.connect(self._on_retry_requested)
        self.window.import_at_path.connect(self.learn_page.open_import_at)

    def _setup_worker(self):
        cfg = load_config()
        self.worker = EvaluationWorker(
            base_url=cfg["base_url"],
            api_key=cfg["api_key"],
            model=cfg["model"],
            prompt_template=cfg["prompt_template"],
        )
        self.worker.evaluation_done.connect(self._on_eval_done)
        self.worker.evaluation_failed.connect(self._on_eval_failed)

        self.eval_thread = EvaluationThread(self.worker)
        self.eval_thread.start()

    def _find_subtitle(self, subtitle_id):
        subs = get_subtitles_for_session(self.learn_page.session_id or 0)
        for s in subs:
            if s["id"] == subtitle_id:
                return s
        return None

    def _build_context(self, sub_row, session_id):
        """Build context with surrounding Chinese subtitles (NO English to avoid confusing AI)."""
        cfg = load_config()
        n = cfg.get("context_n", 1)
        if n == 0:
            return ""
        all_subs = get_subtitles_for_session(session_id)
        current_idx = sub_row["idx"]
        parts = []
        for s in all_subs:
            if s["idx"] < current_idx and s["idx"] >= current_idx - n:
                parts.append(f"前一句: {s['chinese']}")
            elif s["idx"] > current_idx and s["idx"] <= current_idx + n:
                parts.append(f"后一句: {s['chinese']}")
        if parts:
            return "上下文（仅供参考，不参与评分）:\n" + "\n".join(parts)
        return ""

    def _on_translation_submitted(self, eval_id, subtitle_id, user_input, official):
        if eval_id == -1:  # session ended
            session_id = self.learn_page.session_id
            self._load_review(session_id)
            self.learn_page.reset_to_start()
            self.window.navigate_to_review()
            return

        cfg = load_config()
        self.worker.base_url = cfg["base_url"]
        self.worker.api_key = cfg["api_key"]
        self.worker.model = cfg["model"]
        self.worker.prompt_template = cfg["prompt_template"]

        sub_row = self._find_subtitle(subtitle_id)
        context = self._build_context(sub_row, self.learn_page.session_id) if sub_row else ""

        self.worker.add_task(eval_id, 0, user_input, official, context)

    def _on_redo_submitted(self, eval_id, subtitle_id, user_input, official):
        self._on_translation_submitted(eval_id, subtitle_id, user_input, official)

    def _on_retry_requested(self, eval_id, subtitle_id, user_input, official):
        sub_row = self._find_subtitle(subtitle_id)
        context = self._build_context(sub_row, self.learn_page.session_id) if sub_row else ""
        self.worker.add_task(eval_id, 0, user_input, official, context)

    def _on_eval_done(self, eval_id, result):
        try:
            update_evaluation_status(
                eval_id, "done",
                result["meaning_score"],
                result["grammar_score"],
                result["naturalness_score"],
                result["subtitle_style_score"],
                result["analysis"],
                json.dumps(result.get("suggested_expressions", [])),
            )
        except Exception:
            return

        if hasattr(self, 'review_page') and self.review_page.session_id:
            try:
                conn = get_connection()
                row = conn.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id = t.id "
                    "WHERE e.id = ?", (eval_id,)
                ).fetchone()
                conn.close()
                if row:
                    self.review_page.update_evaluation(row[0])
            except Exception:
                pass

    def _on_eval_failed(self, eval_id):
        try:
            update_evaluation_status(eval_id, "failed", error="批改失败")
        except Exception:
            return

        if hasattr(self, 'review_page') and self.review_page.session_id:
            try:
                conn = get_connection()
                row = conn.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id = t.id "
                    "WHERE e.id = ?", (eval_id,)
                ).fetchone()
                conn.close()
                if row:
                    self.review_page.update_evaluation(row[0])
            except Exception:
                pass

    def _load_review(self, session_id):
        if session_id:
            self.review_page.load_session(session_id)

    def run(self):
        self.window.show()


def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    application = App()
    application.run()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
