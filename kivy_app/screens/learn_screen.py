"""
Learn screen - the main translation training interface.
"""
import os
import threading

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from backtranslate.database.connection import init_db
from backtranslate.database.operations import (
    create_session, create_subtitles_batch, create_translation,
    create_evaluation, update_session_completed, clear_session_data,
    get_subtitles_for_session, record_sentence_completed, get_all_stats,
)
from backtranslate.config import load_config, save_config
from backtranslate.srt.parser import parse_srt
from backtranslate.srt.pairing import pair_by_index, pair_by_timecode

Builder.load_string("""
<LearnScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 0

        # Top bar - KakaoBank style (56dp, same bg)
        BoxLayout:
            size_hint_y: None
            height: 56
            padding: [16, 0]
            canvas.before:
                Color:
                    rgba: 0.965, 0.965, 0.965, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '‹ 返回'
                size_hint_x: None
                width: 56
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.067, 0.067, 0.067, 1
                font_name: 'ChineseFont'
                font_size: '18sp'
                on_press: root.go_home()
            Label:
                text: '回译训练'
                font_name: 'ChineseFont'
                font_size: '18sp'
                bold: True
                color: 0.067, 0.067, 0.067, 1
            Widget:
                size_hint_x: None
                width: 56

        # Content area
        BoxLayout:
            orientation: 'vertical'
            padding: [16, 12]
            spacing: 16

            # Import area (shown when no session)
            BoxLayout:
                id: import_area
                orientation: 'vertical'
                spacing: 16
                size_hint_y: None
                height: 240

                Widget:
                    size_hint_y: None
                    height: 40

                Label:
                    text: '点击下方按钮导入中英字幕文件 \\n开始回译训练'
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    color: 0.533, 0.533, 0.533, 1
                    halign: 'center'

                Button:
                    text: '导入字幕文件'
                    size_hint_y: None
                    height: 48
                    background_normal: ''
                    background_color: 0.776, 0.894, 0.827, 1
                    color: 0.067, 0.067, 0.067, 1
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    bold: True
                    on_press: root.import_srt()
                    canvas.before:
                        Color:
                            rgba: 0.776, 0.894, 0.827, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20, 20, 20, 20]

                # Recent sessions
                Label:
                    id: recent_label
                    text: ''
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    color: 0.533, 0.533, 0.533, 1
                    halign: 'center'
                    size_hint_y: None
                    height: 20

            # Translation area (shown during session)
            BoxLayout:
                id: translation_area
                orientation: 'vertical'
                spacing: 12

                # Progress info
                BoxLayout:
                    size_hint_y: None
                    height: 28
                    spacing: 12
                    Label:
                        text: '第 ' + str(root.current_idx) + '/' + str(root.total_count) + ' 句'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.533, 0.533, 0.533, 1
                        size_hint_x: None
                        width: 150
                    ProgressBar:
                        id: progress_bar
                        max: root.total_count
                        value: root.completed_count
                        size_hint_x: 1

                # Chinese sentence - mint green card (KakaoBank style)
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 180
                    padding: [24, 20]
                    spacing: 8
                    canvas.before:
                        Color:
                            rgba: 0.776, 0.894, 0.827, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        id: chinese_label
                        text: ''
                        font_name: 'ChineseFont'
                        font_size: '22sp'
                        color: 0.067, 0.067, 0.067, 1
                        size_hint_y: None
                        height: 130
                        text_size: self.width - 48, None
                        halign: 'left'
                        valign: 'top'

                # Input field - KakaoBank white card style
                TextInput:
                    id: input_field
                    hint_text: '输入英文翻译...'
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    size_hint_y: None
                    height: 52
                    multiline: False
                    background_color: 1, 1, 1, 1
                    foreground_color: 0.067, 0.067, 0.067, 1
                    padding: [20, 14]
                    on_text_validate: root.submit_translation()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20, 20, 20, 20]

                # Action buttons - KakaoBank style
                BoxLayout:
                    size_hint_y: None
                    height: 48
                    spacing: 12
                    Button:
                        text: '跳过'
                        font_name: 'ChineseFont'
                        font_size: '16sp'
                        background_normal: ''
                        background_color: 0.965, 0.965, 0.965, 1
                        color: 0.533, 0.533, 0.533, 1
                        on_press: root.skip_sentence()
                        canvas.before:
                            Color:
                                rgba: 0.965, 0.965, 0.965, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [20, 20, 20, 20]
                    Button:
                        text: '提交'
                        font_name: 'ChineseFont'
                        font_size: '16sp'
                        bold: True
                        background_normal: ''
                        background_color: 0.776, 0.894, 0.827, 1
                        color: 0.067, 0.067, 0.067, 1
                        on_press: root.submit_translation()
                        canvas.before:
                            Color:
                                rgba: 0.776, 0.894, 0.827, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [20, 20, 20, 20]

                # Stats bar - white card
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 100
                    padding: [20, 14]
                    spacing: 8
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]

                    BoxLayout:
                        size_hint_y: None
                        height: 26
                        spacing: 4
                        Label:
                            text: '今日 ' + root.today + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '14sp'
                            bold: True
                            color: 0.067, 0.067, 0.067, 1
                        Label:
                            text: ' | 连续 ' + root.streak + ' 天'
                            font_name: 'ChineseFont'
                            font_size: '14sp'
                            color: 0.533, 0.533, 0.533, 1
                        Label:
                            text: ' | 总计 ' + root.total + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '14sp'
                            color: 0.533, 0.533, 0.533, 1

                    Label:
                        id: encourage_label
                        text: ''
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.533, 0.533, 0.533, 1
                        size_hint_y: None
                        height: 22

                # End session button
                Button:
                    text: '结束学习'
                    size_hint_y: None
                    height: 48
                    background_normal: ''
                    background_color: 0.965, 0.965, 0.965, 1
                    color: 0.91, 0.3, 0.24, 1
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    on_press: root.end_session()
                    canvas.before:
                        Color:
                            rgba: 0.965, 0.965, 0.965, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20, 20, 20, 20]
""")


class LearnScreen(Screen):
    # Properties for data binding
    current_idx = NumericProperty(1)
    total_count = NumericProperty(1)
    completed_count = NumericProperty(0)
    streak = StringProperty("0")
    today = StringProperty("0")
    total = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_id = None
        self.subtitles = []
        self._in_session = False
        self._selected_ch_path = None
        self._selected_en_path = None
        self._select_step = 1
        self._srt_folder = '/'
        self._srt_popup = None
        self._en_srt_popup = None
        self._select_ch_path = None
        self._select_en_path = None

    def on_enter(self):
        """Called when screen becomes visible."""
        self._update_ui_state()
        self._update_stats()

    def _update_ui_state(self):
        """Show/hide import and translation areas."""
        if self._in_session:
            self.ids.import_area.opacity = 0
            self.ids.import_area.disabled = True
            self.ids.import_area.size_hint_y = None
            self.ids.import_area.height = 0

            self.ids.translation_area.opacity = 1
            self.ids.translation_area.disabled = False
            self.ids.translation_area.size_hint_y = 1
        else:
            self.ids.import_area.opacity = 1
            self.ids.import_area.disabled = False
            self.ids.import_area.size_hint_y = None
            self.ids.import_area.height = 240

            self.ids.translation_area.opacity = 0
            self.ids.translation_area.disabled = True
            self.ids.translation_area.size_hint_y = None
            self.ids.translation_area.height = 0

        if not self._in_session:
            # Show recent history
            cfg = load_config()
            recent = cfg.get("recent_pairs", []) or []
            if recent:
                self.ids.recent_label.text = f"最近: {recent[0].get('name', '')}"
            else:
                self.ids.recent_label.text = ""

    def _update_stats(self):
        stats = get_all_stats()
        self.streak = str(stats["streak"])
        self.today = str(stats["today"])
        self.total = str(stats["total"])

    def _show_encouragement(self):
        import random
        messages = [
            "坚持就是胜利！",
            "每一句都在进步！",
            "离目标又近了一步！",
            "今天的努力是明天的底气！",
            "积少成多，你正在变强！",
            "保持这个节奏！",
            "很棒，继续加油！",
            "每一天都在超越昨天的自己！",
            "坚持练习，英语会越来越好！",
            "你在做一件很酷的事！",
            "不积跬步，无以至千里！",
            "又完成一句，离大师更近了！",
            "每一句翻译都是经验的积累！",
            "坚持下去，你就是冠军！",
        ]
        msg = random.choice(messages)
        self.ids.encourage_label.text = msg
        Clock.schedule_once(lambda dt: self._clear_encouragement(msg), 5)

    def _clear_encouragement(self, msg):
        if self.ids.encourage_label.text == msg:
            self.ids.encourage_label.text = ""

    def import_srt(self):
        """Import SRT files using the Kivy FileChooser or Android native picker."""
        from kivy.utils import platform

        if platform == 'android':
            self._import_srt_android()
        else:
            self._import_srt_desktop()

    def _import_srt_android(self):
        """Use Android's native SAF file picker via plyer."""
        from plyer import filechooser
        from kivy.clock import Clock

        def on_selection(selection):
            if not selection:
                return
            path = selection[0]
            if not isinstance(path, str):
                return
            # We need two files: zh.srt and en.srt in the same directory
            folder = os.path.dirname(path)
            self._show_folder_import(folder, path)

        try:
            filechooser.open_file(
                on_selection=on_selection,
                filters=[('SRT files', '*.srt'), ('All files', '*')],
                multiple=False,
            )
        except Exception as e:
            # Fallback to desktop-style chooser if plyer fails
            self._show_popup("选择文件", f"无法打开文件选择器: {e}\n请使用桌面模式导入。")
            self._import_srt_desktop()

    def _show_folder_import(self, folder, first_file):
        """After user picks one SRT, show all SRTs in that folder."""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView
        from kivy.utils import platform

        content = BoxLayout(orientation='vertical', spacing=12, padding=16)

        prompt_label = Label(
            text=f'目录: {folder}\n请选择中文 SRT 文件（第1步）',
            font_name='ChineseFont',
            font_size='16sp',
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
        )
        content.add_widget(prompt_label)

        # List SRT files in folder
        srt_files = [f for f in os.listdir(folder) if f.lower().endswith('.srt')]
        srt_files.sort()

        if not srt_files:
            content.add_widget(Label(
                text='该文件夹中没有 SRT 文件',
                font_name='ChineseFont',
                font_size='16sp',
                color=(0.7, 0.3, 0.3, 1),
                size_hint_y=None,
                height=40,
            ))
            close_btn = Button(
                text='关闭',
                font_name='ChineseFont',
                font_size='16sp',
                size_hint_y=None,
                height=48,
                background_normal='',
                background_color=(0.85, 0.85, 0.85, 1),
                color=(0.3, 0.3, 0.3, 1),
            )
            popup = Popup(title='导入字幕', content=content, size_hint=(0.9, 0.6), auto_dismiss=False)
            close_btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(close_btn)
            popup.open()
            return

        scroll = ScrollView(size_hint=(1, 1))
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for srt_name in srt_files:
            btn = Button(
                text=srt_name,
                font_name='ChineseFont',
                font_size='16sp',
                size_hint_y=None,
                height=52,
                background_normal='',
                background_color=(0.15, 0.15, 0.2, 1),
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                padding=(16, 0),
            )
            btn.srt_path = os.path.join(folder, srt_name)
            btn.bind(on_press=self._on_srt_selected)
            list_layout.add_widget(btn)

        scroll.add_widget(list_layout)
        content.add_widget(scroll)

        popup = Popup(
            title='选择中文 SRT 文件',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False,
        )
        popup.open()
        self._srt_popup = popup
        self._srt_folder = folder

    def _on_srt_selected(self, btn):
        """Handle SRT file selection from the folder list."""
        ch_path = btn.srt_path
        if hasattr(self, '_srt_popup') and self._srt_popup:
            self._srt_popup.dismiss()

        # Now ask for the English SRT
        self._select_ch_path = ch_path
        self._select_en_path = None
        self._select_step = 2

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._show_en_srt_selector(), 0.1)

    def _show_en_srt_selector(self):
        """Show a second popup to select the English SRT."""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView

        content = BoxLayout(orientation='vertical', spacing=12, padding=16)

        prompt_label = Label(
            text=f'请选择对应的英文 SRT 文件（第2步）',
            font_name='ChineseFont',
            font_size='16sp',
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
        )
        content.add_widget(prompt_label)

        folder = self._srt_folder
        srt_files = [f for f in os.listdir(folder) if f.lower().endswith('.srt')]
        srt_files.sort()

        scroll = ScrollView(size_hint=(1, 1))
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for srt_name in srt_files:
            btn = Button(
                text=srt_name,
                font_name='ChineseFont',
                font_size='16sp',
                size_hint_y=None,
                height=52,
                background_normal='',
                background_color=(0.15, 0.15, 0.2, 1),
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                padding=(16, 0),
            )
            btn.srt_path = os.path.join(folder, srt_name)
            btn.bind(on_press=self._on_en_srt_selected)
            list_layout.add_widget(btn)

        scroll.add_widget(list_layout)
        content.add_widget(scroll)

        cancel_btn = Button(
            text='取消',
            font_name='ChineseFont',
            font_size='16sp',
            size_hint_y=None,
            height=48,
            background_normal='',
            background_color=(0.85, 0.85, 0.85, 1),
            color=(0.3, 0.3, 0.3, 1),
        )
        content.add_widget(cancel_btn)

        popup = Popup(
            title='选择英文 SRT 文件',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False,
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()
        self._en_srt_popup = popup

    def _on_en_srt_selected(self, btn):
        """Handle English SRT selection and start import."""
        en_path = btn.srt_path
        if hasattr(self, '_en_srt_popup') and self._en_srt_popup:
            self._en_srt_popup.dismiss()

        self._select_en_path = en_path
        self._selected_ch_path = self._select_ch_path
        self._selected_en_path = self._select_en_path

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._do_import(), 0.1)

    def _import_srt_desktop(self):
        """Desktop-style SRT import using Kivy FileChooser."""
        from kivy.uix.filechooser import FileChooserListView
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput

        content = BoxLayout(orientation='vertical', spacing=10, padding=16)

        prompt_label = Label(
            text='请选择 SRT 文件所在目录',
            font_name='ChineseFont',
            font_size='17sp',
            size_hint_y=None,
            height=36,
            color=(0.8, 0.8, 0.8, 1),
        )
        content.add_widget(prompt_label)

        start_path = os.path.expanduser('~')

        # Path input for quick navigation
        path_input = TextInput(
            text=start_path,
            font_name='ChineseFont',
            font_size='15sp',
            size_hint_y=None,
            height=44,
            multiline=False,
            hint_text='输入路径后回车跳转',
        )
        content.add_widget(path_input)

        # Custom filter: show SRT files (case-insensitive)
        def srt_filter(folder, filename):
            return filename.lower().endswith('.srt')

        filechooser = FileChooserListView(
            filters=[srt_filter],
            path=start_path,
        )
        content.add_widget(filechooser)

        # Toggle filter button
        filter_btn = Button(
            text='仅显示 .srt 文件',
            font_name='ChineseFont',
            font_size='14sp',
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
            color=(0.8, 0.8, 0.8, 1),
        )
        _filter_active = True
        def toggle_filter(btn):
            nonlocal _filter_active
            if _filter_active:
                filechooser.filters = []
                btn.text = '显示所有文件'
            else:
                filechooser.filters = [srt_filter]
                btn.text = '仅显示 .srt 文件'
            _filter_active = not _filter_active
            filechooser._trigger_files_update()
        filter_btn.bind(on_press=toggle_filter)
        content.add_widget(filter_btn)

        # Navigate to path when user presses Enter
        def on_path_submit(instance):
            p = instance.text.strip()
            if os.path.isdir(p):
                filechooser.path = p
            elif os.path.isdir(os.path.dirname(p)):
                filechooser.path = os.path.dirname(p)

        path_input.bind(on_text_validate=on_path_submit)

        btn_layout = BoxLayout(size_hint_y=None, height=44, spacing=12)
        cancel_btn = Button(
            text='取消',
            font_name='ChineseFont',
            background_normal='',
            background_color=(0.85, 0.85, 0.85, 1),
            color=(0.3, 0.3, 0.3, 1),
            font_size='15sp',
        )
        select_btn = Button(
            text='选择中文 SRT',
            font_name='ChineseFont',
            background_normal='',
            background_color=(0.29, 0.56, 0.85, 1),
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True,
        )
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(select_btn)
        content.add_widget(btn_layout)

        popup = Popup(
            title='导入字幕',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False,
        )

        self._selected_ch_path = None
        self._selected_en_path = None
        self._popup = popup
        self._filechooser = filechooser
        self._select_btn = select_btn
        self._select_step = 1

        def on_select(btn):
            selection = filechooser.selection
            if not selection:
                return
            path = selection[0]
            if not path.endswith('.srt'):
                return

            if self._select_step == 1:
                self._selected_ch_path = path
                self._select_step = 2
                btn.text = '选择英文 SRT'
                prompt_label.text = '请选择对应的英文 SRT 文件'
                filechooser.path = os.path.dirname(path)
                filechooser.selection = []
            else:
                self._selected_en_path = path
                popup.dismiss()
                Clock.schedule_once(lambda dt: self._do_import(), 0.1)

        def on_cancel(btn):
            popup.dismiss()
            self._select_step = 1
            self._selected_ch_path = None
            self._selected_en_path = None

        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=on_cancel)

        popup.open()

    def _do_import(self):
        if not self._selected_ch_path or not self._selected_en_path:
            return

        self._select_step = 1
        ch_path = self._selected_ch_path
        en_path = self._selected_en_path

        try:
            with open(ch_path, "r", encoding="utf-8") as f:
                ch_subs = parse_srt(f.read())
            with open(en_path, "r", encoding="utf-8") as f:
                en_subs = parse_srt(f.read())
        except Exception as e:
            self._show_popup("文件错误", f"无法读取字幕文件:\n{e}")
            return

        pairs = pair_by_timecode(ch_subs, en_subs)
        if not pairs:
            pairs = pair_by_index(ch_subs, en_subs)

        if not pairs:
            self._show_popup("配对失败", "没有找到可配对的中英字幕。")
            return

        cfg = load_config()
        recent = list(cfg.get("recent_pairs", []) or [])
        name = os.path.splitext(os.path.basename(ch_path))[0]
        recent = [p for p in recent if not (
            p.get("ch_path") == ch_path and p.get("en_path") == en_path
        )]
        recent.insert(0, {
            "name": name,
            "ch_path": ch_path,
            "en_path": en_path,
            "use_timecode": False,
        })
        cfg["recent_pairs"] = recent[:8]
        save_config(cfg)

        init_db()
        clear_session_data()

        self.session_id = create_session(name, len(pairs))
        self.total_count = len(pairs)
        self.completed_count = 0
        self.current_idx = 1

        self.subtitles = []
        for i, (ch, en) in enumerate(pairs):
            self.subtitles.append({
                "idx": i + 1,
                "chinese": ch["text"],
                "english_official": en["text"],
                "prev_chinese": pairs[i - 1][0]["text"] if i > 0 else "",
                "prev_english": pairs[i - 1][1]["text"] if i > 0 else "",
                "next_chinese": pairs[i + 1][0]["text"] if i < len(pairs) - 1 else "",
                "next_english": pairs[i + 1][1]["text"] if i < len(pairs) - 1 else "",
            })

        create_subtitles_batch(self.session_id, self.subtitles)

        self._in_session = True
        self._update_ui_state()
        self._show_current_sentence()

    def _show_current_sentence(self):
        if self.current_idx > self.total_count:
            self.end_session()
            return
        sub = self.subtitles[self.current_idx - 1]
        self.ids.chinese_label.text = sub["chinese"]
        self.ids.progress_bar.value = self.completed_count
        self.ids.input_field.text = ""
        self.ids.input_field.focus = True

    def submit_translation(self):
        if not self._in_session:
            return
        text = self.ids.input_field.text.strip()
        if not text:
            return

        sub = self.subtitles[self.current_idx - 1]
        subtitle_id = self._get_subtitle_id(self.current_idx)
        if subtitle_id is None:
            return

        translate_id = create_translation(subtitle_id, text, 1)
        eval_id = create_evaluation(translate_id)

        self.completed_count += 1
        self.current_idx += 1

        record_sentence_completed()
        self._update_stats()
        self._show_encouragement()

        if self.session_id:
            update_session_completed(self.session_id, self.completed_count)

        app = self._get_app()
        if app and app.worker:
            context = self._build_context(sub)
            app.worker.add_task(
                eval_id, 0, text, sub["english_official"], context
            )

        self._show_current_sentence()

    def skip_sentence(self):
        if not self._in_session:
            return
        self.completed_count += 1
        self.current_idx += 1
        record_sentence_completed()
        self._update_stats()
        if self.session_id:
            update_session_completed(self.session_id, self.completed_count)
        self._show_current_sentence()

    def end_session(self):
        if not self._in_session:
            return
        self._in_session = False
        self._update_ui_state()

        stats = get_all_stats()
        msg = (
            f"学习小结\n\n"
            f"本次完成：{self.completed_count} 句\n"
            f"今日累计：{stats['today']} 句\n"
            f"连续打卡：{stats['streak']} 天\n"
            f"历史总计：{stats['total']} 句\n"
        )
        if stats['streak'] >= 3:
            msg += f"\n连续 {stats['streak']} 天打卡，太棒了！"
        elif stats['streak'] >= 1:
            msg += "\n今天也打卡成功，明天继续！"
        else:
            msg += "\n明天继续加油！"

        self._show_popup("学习小结", msg)

        self.manager.get_screen("review").load_session(self.session_id, only_translated=True)
        self.manager.current = "review"

    def _build_context(self, sub):
        cfg = load_config()
        n = cfg.get("context_n", 1)
        if n == 0:
            return ""
        parts = []
        for s in self.subtitles:
            idx = s["idx"]
            if idx < self.current_idx - 1 and idx >= self.current_idx - 1 - n:
                parts.append(f"前一句: {s['chinese']}")
            elif idx > self.current_idx - 1 and idx <= self.current_idx - 1 + n:
                parts.append(f"后一句: {s['chinese']}")
        if parts:
            return "上下文（仅供参考，不参与评分）:\n" + "\n".join(parts)
        return ""

    def _get_subtitle_id(self, idx):
        subs = get_subtitles_for_session(self.session_id)
        for s in subs:
            if s["idx"] == idx:
                return s["id"]
        return None

    def _get_app(self):
        from kivy.app import App
        return App.get_running_app()

    def _show_popup(self, title, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', spacing=12, padding=16)
        content.add_widget(Label(
            text=message,
            font_name='ChineseFont',
            font_size='15sp',
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
            text_size=(300, None),
        ))
        btn = Button(
            text='确定',
            font_name='ChineseFont',
            size_hint_y=None,
            height=44,
            background_normal='',
            background_color=(0.29, 0.56, 0.85, 1),
            color=(1, 1, 1, 1),
            font_size='15sp',
        )
        content.add_widget(btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
        )
        btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def go_home(self):
        self.manager.current = "home"

    def load_favorites_review(self, session_id, subtitles):
        """Load favorites as a review session."""
        self.session_id = session_id
        self.subtitles = subtitles
        self.total_count = len(subtitles)
        self.completed_count = 0
        self.current_idx = 1
        self._in_session = True
        self._update_ui_state()
        self._update_stats()
        self._show_current_sentence()