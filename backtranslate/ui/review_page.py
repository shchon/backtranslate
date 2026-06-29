import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QPushButton, QFrame, QLineEdit, QMessageBox,
)
from PySide6.QtCore import Signal, Qt

from backtranslate.database.operations import (
    get_subtitles_for_session, get_latest_translation,
    get_evaluation_for_translation, create_translation,
    create_evaluation, upsert_self_rating, get_self_rating,
    get_all_translations_for_subtitle, add_expression,
)
from backtranslate.database.connection import get_connection


class ReviewPage(QWidget):
    redo_submitted = Signal(int, int, str, str)  # eval_id, subtitle_id, input, official
    retry_requested = Signal(int, int, str, str)  # eval_id, subtitle_id, user_input, official

    def __init__(self):
        super().__init__()
        self.session_id = None
        self.subtitle_rows = []
        self.detail_widgets = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("复盘")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.count_label = QLabel("")
        self.count_label.setStyleSheet("color: #666; margin-bottom: 8px;")
        layout.addWidget(self.count_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.list_container)
        layout.addWidget(scroll)

    def load_session(self, session_id):
        self.session_id = session_id
        self.subtitle_rows = get_subtitles_for_session(session_id)
        self._refresh_list()

    def update_evaluation(self, subtitle_id):
        """Called when a new evaluation result arrives for a specific subtitle."""
        sub = self._subtitle_by_id(subtitle_id)
        if sub is None:
            return
        if str(subtitle_id) in self.detail_widgets:
            old_widget = self.detail_widgets[str(subtitle_id)]
            idx = self.list_layout.indexOf(old_widget)
            if idx >= 0:
                self.list_layout.takeAt(idx)
            old_widget.deleteLater()
        new_widget = self._build_row_widget(sub)
        self.list_layout.insertWidget(0, new_widget)
        self.detail_widgets[str(subtitle_id)] = new_widget

    def _refresh_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.detail_widgets.clear()

        completed = 0
        for sub in self.subtitle_rows:
            eval_data = self._get_latest_eval(sub["id"])
            if eval_data and eval_data["status"] == "done":
                completed += 1
            row_widget = self._build_row_widget(sub)
            self.list_layout.addWidget(row_widget)
            self.detail_widgets[str(sub["id"])] = row_widget

        self.count_label.setText(f"共 {len(self.subtitle_rows)} 句，已批改 {completed} 句")

    def _get_latest_eval(self, subtitle_id):
        tid = self._get_latest_translation_id(subtitle_id)
        if tid is None:
            return None
        return get_evaluation_for_translation(tid)

    def _get_latest_translation_id(self, subtitle_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT id FROM translations WHERE subtitle_id = ? ORDER BY version DESC LIMIT 1",
            (subtitle_id,),
        ).fetchone()
        conn.close()
        return row[0] if row else None

    def _subtitle_by_id(self, sub_id):
        for s in self.subtitle_rows:
            if s["id"] == sub_id:
                return s
        return None

    def _build_row_widget(self, sub):
        frame = QFrame()
        frame.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 6px; margin: 4px 0; }")
        main_layout = QVBoxLayout(frame)

        # Summary row
        summary = QHBoxLayout()
        summary.addWidget(QLabel(f"#{sub['idx']}"))
        ch_label = QLabel(sub["chinese"])
        ch_label.setStyleSheet("font-size: 14px;")
        summary.addWidget(ch_label, 1)

        eval_data = self._get_latest_eval(sub["id"])
        self._add_score_summary(summary, eval_data, sub)
        main_layout.addLayout(summary)

        # Detail area
        detail = QWidget()
        self._build_detail_content(detail, sub, eval_data)
        main_layout.addWidget(detail)

        return frame

    def _add_score_summary(self, layout, eval_data, sub):
        if eval_data is None or eval_data["status"] == "pending":
            lbl = QLabel("⏳ 等待批改")
            lbl.setStyleSheet("color: #888;")
            layout.addWidget(lbl)
        elif eval_data["status"] == "processing":
            lbl = QLabel("\U0001f504 批改中")
            lbl.setStyleSheet("color: #f39c12;")
            layout.addWidget(lbl)
        elif eval_data["status"] == "failed":
            lbl = QLabel("❌ 批改失败")
            lbl.setStyleSheet("color: #e74c3c;")
            layout.addWidget(lbl)
            retry_btn = QPushButton("重试")
            retry_btn.setStyleSheet(
                "color: #e74c3c; border: 1px solid #e74c3c; border-radius: 3px; padding: 2px 8px;"
            )
            retry_btn.clicked.connect(lambda checked, s=sub, e=eval_data: self._retry_eval(s, e))
            layout.addWidget(retry_btn)
        elif eval_data["status"] == "done":
            avg = (
                eval_data["meaning_score"] + eval_data["grammar_score"]
                + eval_data["naturalness_score"] + eval_data["subtitle_style_score"]
            ) / 4
            color = "#27ae60" if avg >= 80 else "#f39c12" if avg >= 60 else "#e74c3c"
            lbl = QLabel(f"综合 {avg:.0f}")
            lbl.setStyleSheet(f"color: {color}; font-weight: bold;")
            layout.addWidget(lbl)

    def _build_detail_content(self, parent, sub, eval_data):
        parent_layout = QVBoxLayout(parent)

        if eval_data and eval_data["status"] == "done":
            scores_text = (
                f"意思: {eval_data['meaning_score']} | "
                f"语法: {eval_data['grammar_score']} | "
                f"自然度: {eval_data['naturalness_score']} | "
                f"字幕风格: {eval_data['subtitle_style_score']}"
            )
            scores_label = QLabel(scores_text)
            scores_label.setStyleSheet("font-size: 13px; margin-bottom: 8px;")
            parent_layout.addWidget(scores_label)

            analysis_label = QLabel(eval_data["analysis_text"] or "")
            analysis_label.setWordWrap(True)
            analysis_label.setStyleSheet("color: #333; margin-bottom: 8px;")
            parent_layout.addWidget(analysis_label)

        # Official subtitle (hidden by default)
        official_btn = QPushButton("查看官方字幕")
        official_btn.setStyleSheet("color: #4a90d9; border: none;")
        official_label = QLabel(sub["english_official"])
        official_label.setWordWrap(True)
        official_label.setVisible(False)
        parent_layout.addWidget(official_btn)
        parent_layout.addWidget(official_label)
        official_btn.clicked.connect(
            lambda: official_label.setVisible(not official_label.isVisible())
        )

        # Self rating
        rating_layout = QHBoxLayout()
        for emoji, val in [("\U0001f60a", 3), ("\U0001f610", 2), ("\U0001f613", 1)]:
            btn = QPushButton(emoji)
            btn.setFixedSize(36, 36)
            btn.clicked.connect(
                lambda checked, s=sub["id"], v=val: upsert_self_rating(s, v)
            )
            rating_layout.addWidget(btn)
        parent_layout.addWidget(QLabel("自我评分:"))
        parent_layout.addLayout(rating_layout)

        # Redo
        redo_layout = QHBoxLayout()
        redo_input = QLineEdit()
        redo_input.setPlaceholderText("重新翻译...")
        redo_btn = QPushButton("提交")
        redo_btn.clicked.connect(lambda: self._submit_redo(sub, redo_input))
        redo_layout.addWidget(redo_input, 1)
        redo_layout.addWidget(redo_btn)
        parent_layout.addLayout(redo_layout)

        # Version history
        versions = get_all_translations_for_subtitle(sub["id"])
        if len(versions) > 1:
            ver_label = QLabel(f"共 {len(versions)} 个版本:")
            ver_label.setStyleSheet("color: #666; font-size: 12px;")
            parent_layout.addWidget(ver_label)
            for v in versions:
                parent_layout.addWidget(QLabel(f"  v{v['version']}: {v['user_input']}"))

        # Collect expression
        if eval_data and eval_data.get("suggested_expressions"):
            try:
                suggested = json.loads(eval_data["suggested_expressions"])
            except (json.JSONDecodeError, TypeError):
                suggested = []
            for expr in suggested:
                collect_btn = QPushButton(f"收藏: {expr}")
                collect_btn.clicked.connect(
                    lambda checked, e=expr, s=sub["id"]: self._collect(e, s)
                )
                parent_layout.addWidget(collect_btn)

        # Manual collect
        manual_layout = QHBoxLayout()
        manual_input = QLineEdit()
        manual_input.setPlaceholderText("手动添加表达...")
        add_btn = QPushButton("添加")
        add_btn.clicked.connect(lambda: self._collect(manual_input.text(), sub["id"]))
        manual_layout.addWidget(manual_input, 1)
        manual_layout.addWidget(add_btn)
        parent_layout.addLayout(manual_layout)

    def _retry_eval(self, sub, eval_data):
        translation = get_latest_translation(sub["id"])
        if translation:
            from backtranslate.database.operations import update_evaluation_status
            update_evaluation_status(eval_data["id"], "pending")
            self.retry_requested.emit(
                eval_data["id"], sub["id"], translation, sub["english_official"]
            )

    def _submit_redo(self, sub, input_widget):
        text = input_widget.text().strip()
        if not text:
            return
        tid = self._get_latest_translation_id(sub["id"])
        version = 1
        if tid:
            conn = get_connection()
            row = conn.execute(
                "SELECT MAX(version) FROM translations WHERE subtitle_id = ?",
                (sub["id"],),
            ).fetchone()
            conn.close()
            version = (row[0] or 0) + 1

        translate_id = create_translation(sub["id"], text, version)
        eval_id = create_evaluation(translate_id)
        self.redo_submitted.emit(eval_id, sub["id"], text, sub["english_official"])
        input_widget.clear()
        QMessageBox.information(self, "已提交", "重新翻译已提交 AI 批改。")

    def _collect(self, phrase, subtitle_id):
        if phrase and phrase.strip():
            add_expression(phrase.strip(), subtitle_id)
            QMessageBox.information(self, "已收藏", f"已收藏: {phrase}")
