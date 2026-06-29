from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QProgressBar, QFileDialog, QMessageBox,
    QDialog, QRadioButton, QGroupBox,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from backtranslate.srt.parser import parse_srt
from backtranslate.srt.pairing import pair_by_index, pair_by_timecode
from backtranslate.database.connection import init_db
from backtranslate.database.operations import (
    create_session, create_subtitles_batch, create_translation,
    create_evaluation, update_session_completed, clear_session_data,
    get_subtitles_for_session,
)


class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("导入字幕")
        self.resize(500, 250)
        self.chinese_path = ""
        self.english_path = ""

        layout = QVBoxLayout(self)

        # Chinese SRT
        layout.addWidget(QLabel("中文 SRT 文件:"))
        ch_layout = QHBoxLayout()
        self.ch_path_label = QLabel("未选择")
        self.ch_path_label.setStyleSheet("color: #999;")
        ch_layout.addWidget(self.ch_path_label)
        ch_btn = QPushButton("选择...")
        ch_btn.clicked.connect(self._select_chinese)
        ch_layout.addWidget(ch_btn)
        layout.addLayout(ch_layout)

        # English SRT
        layout.addWidget(QLabel("英文 SRT 文件:"))
        en_layout = QHBoxLayout()
        self.en_path_label = QLabel("未选择")
        self.en_path_label.setStyleSheet("color: #999;")
        en_layout.addWidget(self.en_path_label)
        en_btn = QPushButton("选择...")
        en_btn.clicked.connect(self._select_english)
        en_layout.addWidget(en_btn)
        layout.addLayout(en_layout)

        # Pairing strategy
        pair_group = QGroupBox("配对策略")
        pair_layout = QVBoxLayout(pair_group)
        self.by_timecode_rb = QRadioButton("按时间轴匹配")
        self.by_index_rb = QRadioButton("按序号匹配")
        self.by_timecode_rb.setChecked(True)
        pair_layout.addWidget(self.by_timecode_rb)
        pair_layout.addWidget(self.by_index_rb)
        layout.addWidget(pair_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        self.ok_btn = QPushButton("开始学习")
        self.ok_btn.setStyleSheet(
            "QPushButton { background: #4a90d9; color: white; padding: 8px 20px; "
            "border-radius: 4px; }"
        )
        self.ok_btn.clicked.connect(self._validate)
        btn_layout.addWidget(self.ok_btn)
        layout.addLayout(btn_layout)

    def _select_chinese(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择中文 SRT", "", "SRT Files (*.srt)")
        if path:
            self.chinese_path = path
            self.ch_path_label.setText(path)
            self.ch_path_label.setStyleSheet("color: #333;")

    def _select_english(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择英文 SRT", "", "SRT Files (*.srt)")
        if path:
            self.english_path = path
            self.en_path_label.setText(path)
            self.en_path_label.setStyleSheet("color: #333;")

    def _validate(self):
        if not self.chinese_path or not self.english_path:
            QMessageBox.warning(self, "提示", "请选择中文和英文 SRT 文件。")
            return
        self.accept()


class LearnPage(QWidget):
    session_created = Signal(int, int)   # session_id, total count
    translation_submitted = Signal(int, int, str, str)  # eval_id, subtitle_id, user_input, official

    def __init__(self):
        super().__init__()
        self.session_id = None
        self.subtitles = []
        self.current_idx = 0
        self.total_count = 0
        self.completed_count = 0
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        # Top bar
        top = QHBoxLayout()
        self.title_label = QLabel("回译训练")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        top.addWidget(self.title_label)
        top.addStretch()

        self.import_btn = QPushButton("导入字幕")
        self.import_btn.setStyleSheet(
            "QPushButton { background: #4a90d9; color: white; padding: 8px 16px; "
            "border-radius: 4px; font-size: 14px; }"
            "QPushButton:hover { background: #357abd; }"
        )
        self.import_btn.clicked.connect(self._show_import_dialog)
        top.addWidget(self.import_btn)

        self.end_btn = QPushButton("结束学习")
        self.end_btn.setStyleSheet(
            "QPushButton { background: #e74c3c; color: white; padding: 8px 16px; "
            "border-radius: 4px; font-size: 14px; }"
            "QPushButton:hover { background: #c0392b; }"
        )
        self.end_btn.clicked.connect(self._end_session)
        self.end_btn.setVisible(False)
        top.addWidget(self.end_btn)

        layout.addLayout(top)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #666;")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        # Translation area
        self.translation_area = QWidget()
        self.translation_area.setVisible(False)
        ta_layout = QVBoxLayout(self.translation_area)
        ta_layout.setContentsMargins(0, 12, 0, 0)

        self.chinese_label = QLabel("")
        font = QFont()
        font.setPointSize(18)
        self.chinese_label.setFont(font)
        self.chinese_label.setAlignment(Qt.AlignCenter)
        self.chinese_label.setMinimumHeight(80)
        self.chinese_label.setWordWrap(True)
        ta_layout.addWidget(self.chinese_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入英文翻译，按 Enter 提交...")
        self.input_field.setMinimumHeight(44)
        input_font = QFont()
        input_font.setPointSize(14)
        self.input_field.setFont(input_font)
        self.input_field.returnPressed.connect(self._submit_translation)
        ta_layout.addWidget(self.input_field)

        # Buttons below input
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        skip_btn = QPushButton("跳过")
        skip_btn.setStyleSheet(
            "QPushButton { color: #888; border: 1px solid #ccc; "
            "padding: 8px 20px; border-radius: 4px; font-size: 13px; }"
            "QPushButton:hover { background: #eee; }"
        )
        skip_btn.clicked.connect(self._skip_sentence)
        btn_row.addWidget(skip_btn)
        next_btn = QPushButton("下一句")
        next_btn.setStyleSheet(
            "QPushButton { background: #4a90d9; color: white; "
            "padding: 8px 24px; border-radius: 4px; font-size: 13px; }"
            "QPushButton:hover { background: #357abd; }"
        )
        next_btn.clicked.connect(self._submit_translation)
        btn_row.addWidget(next_btn)
        ta_layout.addLayout(btn_row)

        layout.addWidget(self.translation_area)

        # Empty state
        self.empty_label = QLabel("点击\"导入字幕\"开始学习")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #999; font-size: 16px;")
        layout.addWidget(self.empty_label)

        layout.addStretch()

    def _show_import_dialog(self):
        dlg = ImportDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self._import_srt(dlg.chinese_path, dlg.english_path, dlg.by_timecode_rb.isChecked())

    def _import_srt(self, ch_path, en_path, use_timecode):
        try:
            with open(ch_path, "r", encoding="utf-8") as f:
                ch_subs = parse_srt(f.read())
            with open(en_path, "r", encoding="utf-8") as f:
                en_subs = parse_srt(f.read())
        except (OSError, UnicodeDecodeError) as e:
            QMessageBox.critical(self, "文件错误", f"无法读取字幕文件:\n{e}")
            return

        if use_timecode:
            pairs = pair_by_timecode(ch_subs, en_subs)
        else:
            pairs = pair_by_index(ch_subs, en_subs)

        if not pairs:
            QMessageBox.warning(self, "配对失败", "没有找到可配对的中英字幕。")
            return

        # Show preview for user to verify pairing before starting
        preview_lines = []
        preview_count = min(5, len(pairs))
        for i in range(preview_count):
            ch_text = pairs[i][0]["text"]
            en_text = pairs[i][1]["text"]
            preview_lines.append(f"#{i + 1}  {ch_text}")
            preview_lines.append(f"    {en_text}")

        preview_text = "\n".join(preview_lines)
        summary = (
            f"中文 {len(ch_subs)} 句，英文 {len(en_subs)} 句 → 配对 {len(pairs)} 句\n\n"
            f"前 {preview_count} 句预览:\n{preview_text}"
        )
        if len(ch_subs) != len(en_subs):
            summary += (
                f"\n\n⚠ 中英句数不一致！"
                f"\n中文 {len(ch_subs)} 句，英文 {len(en_subs)} 句"
                f"\n请检查是否选错了文件，或尝试「按时间轴匹配」。"
            )

        reply = QMessageBox.question(
            self, "确认配对结果", summary,
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if reply != QMessageBox.Ok:
            return

        init_db()
        import os
        name = os.path.splitext(os.path.basename(ch_path))[0]

        clear_session_data()

        self.session_id = create_session(name, len(pairs))
        self.total_count = len(pairs)
        self.completed_count = 0
        self.current_idx = 0

        self.subtitles = []
        for i, (ch, en) in enumerate(pairs):
            prev_ch = pairs[i - 1][0]["text"] if i > 0 else ""
            prev_en = pairs[i - 1][1]["text"] if i > 0 else ""
            next_ch = pairs[i + 1][0]["text"] if i < len(pairs) - 1 else ""
            next_en = pairs[i + 1][1]["text"] if i < len(pairs) - 1 else ""

            self.subtitles.append({
                "idx": i + 1,
                "chinese": ch["text"],
                "english_official": en["text"],
                "prev_chinese": prev_ch,
                "prev_english": prev_en,
                "next_chinese": next_ch,
                "next_english": next_en,
            })

        create_subtitles_batch(self.session_id, self.subtitles)
        self.session_created.emit(self.session_id, self.total_count)

        self._start_translation_ui()

    def _start_translation_ui(self):
        self.import_btn.setVisible(False)
        self.empty_label.setVisible(False)
        self.translation_area.setVisible(True)
        self.end_btn.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(self.total_count)
        self.progress_label.setVisible(True)
        self._show_current_sentence()

    def _show_current_sentence(self):
        if self.current_idx >= self.total_count:
            self._end_session()
            return
        sub = self.subtitles[self.current_idx]
        self.chinese_label.setText(sub["chinese"])
        self.progress_bar.setValue(self.completed_count)
        self.progress_label.setText(f"第 {self.current_idx + 1}/{self.total_count} 句")
        self.input_field.clear()
        self.input_field.setFocus()

    def _submit_translation(self):
        text = self.input_field.text().strip()
        if not text:
            return

        # 统一从 DB 读取，确保发给 AI 的官方字幕与复盘页显示一致
        subs_row = self._get_subtitle_row(self.current_idx + 1)
        if subs_row is None:
            return

        translate_id = create_translation(subs_row["id"], text, 1)
        eval_id = create_evaluation(translate_id)

        self.completed_count += 1
        self.current_idx += 1

        if self.session_id:
            update_session_completed(self.session_id, self.completed_count)

        self.translation_submitted.emit(
            eval_id, subs_row["id"], text, subs_row["english_official"]
        )

        self._show_current_sentence()

    def _skip_sentence(self):
        """Skip current sentence without translating."""
        self.completed_count += 1
        self.current_idx += 1
        if self.session_id:
            update_session_completed(self.session_id, self.completed_count)
        self._show_current_sentence()

    def _get_subtitle_row(self, idx):
        subs = get_subtitles_for_session(self.session_id)
        for s in subs:
            if s["idx"] == idx:
                return s
        return None

    def _end_session(self):
        self.input_field.setEnabled(False)
        self.translation_submitted.emit(-1, -1, "", "")  # sentinel for "session ended"

    def reset_to_start(self):
        self.session_id = None
        self.subtitles = []
        self.current_idx = 0
        self.total_count = 0
        self.completed_count = 0
        self.import_btn.setVisible(True)
        self.empty_label.setVisible(True)
        self.translation_area.setVisible(False)
        self.end_btn.setVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.input_field.setEnabled(True)
        self.input_field.clear()
