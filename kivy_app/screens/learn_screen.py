"""Learn screen — clean modern training interface."""
import os
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle

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
        canvas.before:
            Color:
                rgba: 0.969, 0.973, 0.969, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # Top bar
        BoxLayout:
            size_hint_y: None
            height: 56
            padding: [12, 0]
            canvas.before:
                Color:
                    rgba: 0.969, 0.973, 0.969, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '← 返回'
                size_hint_x: None
                width: 64
                background_normal: ''
                background_color: 0,0,0,0
                color: 0.420, 0.565, 0.502, 1
                font_name: 'ChineseFont'
                font_size: '16sp'
                on_press: root.go_home()
            Label:
                text: '回译学习'
                font_name: 'ChineseFont'
                font_size: '20sp'
                bold: True
                color: 0.067, 0.078, 0.086, 1
            Widget:
                size_hint_x: None
                width: 88

        # Import area (shown when no session)
        BoxLayout:
            id: import_area
            orientation: 'vertical'
            spacing: 16
            size_hint_y: None
            height: 280
            padding: [16, 12]

            Widget:
                size_hint_y: None
                height: 40

            Label:
                text: '导入中英字幕文件\\n开始回译训练'
                font_name: 'ChineseFont'
                font_size: '15sp'
                color: 0.302, 0.325, 0.349, 1
                halign: 'center'

            Button:
                text: '选择字幕文件'
                font_name: 'ChineseFont'
                font_size: '16sp'
                bold: True
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.420, 0.565, 0.502, 1
                size_hint_y: None
                height: 48
                on_press: root.import_srt()
                canvas.before:
                    Color:
                        rgba: 0.420, 0.565, 0.502, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12, 12, 12, 12]

            Label:
                id: recent_label
                text: ''
                font_name: 'ChineseFont'
                font_size: '13sp'
                color: 0.420, 0.447, 0.475, 1
                halign: 'center'
                size_hint_y: None
                height: 20

        # Translation area (shown during session)
        BoxLayout:
            id: translation_area
            orientation: 'vertical'
            spacing: 12
            padding: [16, 12]

            # Progress
            Label:
                id: progress_label
                text: '第 ' + str(root.current_idx) + '/' + str(root.total_count) + ' 句'
                font_name: 'ChineseFont'
                font_size: '13sp'
                color: 0.302, 0.325, 0.349, 1
                size_hint_y: None
                height: 28

            # Sentence card
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: 200
                padding: [20, 18]
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [16, 16, 16, 16]
                Label:
                    id: chinese_label
                    text: ''
                    font_name: 'ChineseFont'
                    font_size: '22sp'
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 160
                    text_size: self.width - 40, None
                    halign: 'left'
                    valign: 'top'

            # Input
            TextInput:
                id: input_field
                hint_text: '输入英文翻译……'
                hint_text_color: 0.420, 0.447, 0.475, 1
                font_name: 'ChineseFont'
                font_size: '16sp'
                size_hint_y: None
                height: 52
                multiline: False
                background_color: 1, 1, 1, 1
                foreground_color: 0, 0, 0, 1
                padding: [20, 14]
                on_text_validate: root.submit_translation()

            # Action buttons
            BoxLayout:
                size_hint_y: None
                height: 48
                spacing: 12
                Button:
                    text: '跳过'
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    color: 0.302, 0.325, 0.349, 1
                    background_normal: ''
                    background_color: 0.890, 0.898, 0.886, 1
                    on_press: root.skip_sentence()
                    canvas.before:
                        Color:
                            rgba: 0.890, 0.898, 0.886, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]
                Button:
                    text: '提交'
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    bold: True
                    color: 1, 1, 1, 1
                    background_normal: ''
                    background_color: 0.420, 0.565, 0.502, 1
                    on_press: root.submit_translation()
                    canvas.before:
                        Color:
                            rgba: 0.420, 0.565, 0.502, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

            # Stats
            BoxLayout:
                size_hint_y: None
                height: 24
                spacing: 12
                Label:
                    text: '今日 ' + root.today + ' 句'
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    bold: True
                    color: 0.420, 0.565, 0.502, 1
                    size_hint_x: None
                    width: 120
                    halign: 'left'
                Label:
                    text: '|  连续 ' + root.streak + ' 天'
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    color: 0.420, 0.447, 0.475, 1
                    size_hint_x: None
                    width: 120
                    halign: 'left'
                Label:
                    id: encourage_label
                    text: ''
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    color: 0.302, 0.325, 0.349, 1

            # End
            Button:
                text: '结束学习'
                size_hint_y: None
                height: 48
                font_name: 'ChineseFont'
                font_size: '15sp'
                color: 0.878, 0.345, 0.298, 1
                background_normal: ''
                background_color: 0.890, 0.898, 0.886, 1
                on_press: root.end_session()
                canvas.before:
                    Color:
                        rgba: 0.890, 0.898, 0.886, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12, 12, 12, 12]
""")


class LearnScreen(Screen):
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
        self._update_ui_state()
        self._update_stats()

    def _update_ui_state(self):
        if self._in_session:
            self.ids.import_area.height = 0
            self.ids.import_area.disabled = True
            self.ids.translation_area.disabled = False
        else:
            self.ids.import_area.height = 280
            self.ids.import_area.disabled = False
            self.ids.translation_area.disabled = True

    def _update_stats(self):
        stats = get_all_stats()
        self.streak = str(stats["streak"])
        self.today = str(stats["today"])
        self.total = str(stats["total"])

    def _show_encouragement(self):
        import random
        msgs = ["坚持就是胜利！","每一句都在进步！","离目标又近了一步！",
                "今天的努力是明天的底气！","积少成多，你正在变强！",
                "保持这个节奏！","很棒，继续加油！",
                "坚持练习，英语会越来越好！","不积跬步，无以至千里！"]
        msg = random.choice(msgs)
        self.ids.encourage_label.text = msg
        Clock.schedule_once(lambda dt: self._clear_encouragement(msg), 5)

    def _clear_encouragement(self, msg):
        if self.ids.encourage_label.text == msg:
            self.ids.encourage_label.text = ""

    def import_srt(self):
        from kivy.utils import platform
        if platform == 'android':
            self._import_srt_android()
        else:
            self._import_srt_desktop()

    def _import_srt_android(self):
        from plyer import filechooser
        try:
            filechooser.open_file(
                on_selection=lambda sel:
                    self._show_folder_import(os.path.dirname(sel[0]), sel[0]) if sel else None,
                filters=[('SRT files', '*.srt')], multiple=False)
        except:
            self._import_srt_desktop()

    def _show_folder_import(self, folder, _first_file):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView

        content = BoxLayout(orientation='vertical', spacing=12, padding=16)
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16]*4)
        content.add_widget(Label(text='选择中文 SRT（第1步）',
            font_name='ChineseFont', font_size='15sp', size_hint_y=None, height=40,
            color=(0.067, 0.078, 0.086, 1)))

        files = sorted(f for f in os.listdir(folder) if f.lower().endswith('.srt'))
        if not files:
            content.add_widget(Label(text='该目录无 SRT 文件', font_name='ChineseFont',
                size_hint_y=None, height=40, color=(0.878, 0.345, 0.298, 1)))
            popup = Popup(title='导入字幕', content=content, size_hint=(0.85, 0.5), auto_dismiss=False)
            popup.title_color = (0.067, 0.078, 0.086, 1)
            btn = Button(text='关闭', font_name='ChineseFont', size_hint_y=None, height=44,
                background_normal='', background_color=(0.95,0.95,0.95,1), color=(0.4,0.4,0.4,1))
            btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(btn)
            popup.open()
            return

        scroll = ScrollView(size_hint=(1, 1))
        lst = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        lst.bind(minimum_height=lst.setter('height'))
        for s in files:
            btn = Button(text=s, font_name='ChineseFont', font_size='15sp',
                size_hint_y=None, height=48,
                background_normal='', background_color=(0.890,0.898,0.886,1),
                color=(0.067,0.078,0.086,1), halign='left', padding=(16,0))
            btn.srt_path = os.path.join(folder, s)
            btn.bind(on_press=self._on_srt_selected)
            lst.add_widget(btn)
        scroll.add_widget(lst)
        content.add_widget(scroll)

        popup = Popup(title='选择中文 SRT', content=content, size_hint=(0.9, 0.8), auto_dismiss=False)
        popup.background_color = (0.969, 0.973, 0.969, 1)
        popup.separator_color = (0.890, 0.898, 0.886, 1)
        popup.title_color = (0.067, 0.078, 0.086, 1)
        popup.open()
        self._srt_popup = popup
        self._srt_folder = folder

    def _on_srt_selected(self, btn):
        ch = btn.srt_path
        if self._srt_popup:
            self._srt_popup.dismiss()
        self._select_ch_path = ch
        Clock.schedule_once(lambda dt: self._show_en_srt_selector(), 0.1)

    def _show_en_srt_selector(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView

        content = BoxLayout(orientation='vertical', spacing=12, padding=16)
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16]*4)
        content.add_widget(Label(text='选择英文 SRT（第2步）',
            font_name='ChineseFont', font_size='15sp', size_hint_y=None, height=40,
            color=(0.067,0.078,0.086,1)))

        files = sorted(f for f in os.listdir(self._srt_folder) if f.lower().endswith('.srt'))
        scroll = ScrollView(size_hint=(1, 1))
        lst = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        lst.bind(minimum_height=lst.setter('height'))
        for s in files:
            btn = Button(text=s, font_name='ChineseFont', font_size='15sp',
                size_hint_y=None, height=48,
                background_normal='', background_color=(0.890,0.898,0.886,1),
                color=(0.067,0.078,0.086,1), halign='left', padding=(16,0))
            btn.srt_path = os.path.join(self._srt_folder, s)
            btn.bind(on_press=self._on_en_srt_selected)
            lst.add_widget(btn)
        scroll.add_widget(lst)
        content.add_widget(scroll)

        cancel = Button(text='取消', font_name='ChineseFont', size_hint_y=None, height=44,
            background_normal='', background_color=(0.95,0.95,0.95,1), color=(0.4,0.4,0.4,1))
        content.add_widget(cancel)
        popup = Popup(title='选择英文 SRT', content=content, size_hint=(0.9, 0.8), auto_dismiss=False)
        popup.background_color = (0.969, 0.973, 0.969, 1)
        popup.separator_color = (0.890, 0.898, 0.886, 1)
        popup.title_color = (0.067, 0.078, 0.086, 1)
        cancel.bind(on_press=lambda x: popup.dismiss())
        popup.open()
        self._en_srt_popup = popup

    def _on_en_srt_selected(self, btn):
        en = btn.srt_path
        if self._en_srt_popup:
            self._en_srt_popup.dismiss()
        self._select_en_path = en
        self._selected_ch_path = self._select_ch_path
        self._selected_en_path = en
        Clock.schedule_once(lambda dt: self._do_import(), 0.1)

    def _import_srt_desktop(self):
        from kivy.uix.filechooser import FileChooserListView
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput

        content = BoxLayout(orientation='vertical', spacing=10, padding=16)
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16]*4)
        content.add_widget(Label(text='选择 SRT 目录', font_name='ChineseFont',
            font_size='15sp', size_hint_y=None, height=36, color=(0.067, 0.078, 0.086, 1)))

        pi = TextInput(text=os.path.expanduser('~'), font_name='ChineseFont', font_size='14sp',
            size_hint_y=None, height=44, multiline=False, hint_text='输入路径')
        content.add_widget(pi)

        fc = FileChooserListView(filters=[lambda f, n: n.lower().endswith('.srt')], path=os.path.expanduser('~'))
        content.add_widget(fc)

        btns = BoxLayout(size_hint_y=None, height=44, spacing=12)
        cancel = Button(text='取消', font_name='ChineseFont', font_size='15sp',
            background_normal='', background_color=(0.95,0.95,0.95,1), color=(0.4,0.4,0.4,1))
        select = Button(text='选择中文 SRT', font_name='ChineseFont', font_size='15sp', bold=True,
            background_normal='', background_color=(0.420,0.565,0.502,1), color=(1,1,1,1))
        btns.add_widget(cancel)
        btns.add_widget(select)
        content.add_widget(btns)

        popup = Popup(title='导入字幕', content=content, size_hint=(0.9, 0.8), auto_dismiss=False)
        popup.background_color = (0.969, 0.973, 0.969, 1)
        popup.separator_color = (0.890, 0.898, 0.886, 1)
        popup.title_color = (0.067, 0.078, 0.086, 1)
        self._selected_ch_path = None
        self._selected_en_path = None
        self._select_step = 1

        def on_goto(inst):
            p = inst.text.strip()
            if os.path.isdir(p):
                fc.path = p
        pi.bind(on_text_validate=on_goto)

        def on_s(btn):
            sel = fc.selection
            if not sel or not sel[0].endswith('.srt'):
                return
            if self._select_step == 1:
                self._selected_ch_path = sel[0]
                self._select_step = 2
                btn.text = '选择英文 SRT'
                fc.path = os.path.dirname(sel[0])
                fc.selection = []
            else:
                self._selected_en_path = sel[0]
                popup.dismiss()
                Clock.schedule_once(lambda dt: self._do_import(), 0.1)

        select.bind(on_press=on_s)
        cancel.bind(on_press=lambda x: [setattr(self, '_select_step', 1), popup.dismiss()])
        popup.open()

    def _do_import(self):
        if not self._selected_ch_path or not self._selected_en_path:
            return
        self._select_step = 1
        try:
            with open(self._selected_ch_path, 'r', encoding='utf-8') as f:
                ch_s = parse_srt(f.read())
            with open(self._selected_en_path, 'r', encoding='utf-8') as f:
                en_s = parse_srt(f.read())
        except Exception as e:
            self._show_popup("文件错误", f"无法读取字幕文件:\\n{e}")
            return

        pairs = pair_by_timecode(ch_s, en_s) or pair_by_index(ch_s, en_s)
        if not pairs:
            self._show_popup("配对失败", "没有找到可配对的中英字幕。")
            return

        cfg = load_config()
        recent = list(cfg.get("recent_pairs", []) or [])
        name = os.path.splitext(os.path.basename(self._selected_ch_path))[0]
        recent.insert(0, {"name": name, "ch_path": self._selected_ch_path, "en_path": self._selected_en_path})
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
            self.subtitles.append({"idx": i+1, "chinese": ch["text"], "english_official": en["text"],
                "prev_chinese": pairs[i-1][0]["text"] if i>0 else "",
                "next_chinese": pairs[i+1][0]["text"] if i<len(pairs)-1 else ""})
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
        self.ids.input_field.text = ""
        self.ids.input_field.focus = True

    def submit_translation(self):
        if not self._in_session:
            return
        text = self.ids.input_field.text.strip()
        if not text:
            return
        sub = self.subtitles[self.current_idx - 1]
        sid = self._get_subtitle_id(self.current_idx)
        if sid is None:
            return
        tid = create_translation(sid, text, 1)
        eid = create_evaluation(tid)
        self.completed_count += 1
        self.current_idx += 1
        record_sentence_completed()
        self._update_stats()
        self._show_encouragement()
        if self.session_id:
            update_session_completed(self.session_id, self.completed_count)
        app = self._get_app()
        if app and app.worker:
            app.worker.add_task(eid, 0, text, sub["english_official"], self._build_context(sub))
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
        msg = (f"学习小结\\n\\n本次完成：{self.completed_count} 句\\n"
               f"今日累计：{stats['today']} 句\\n连续打卡：{stats['streak']} 天\\n"
               f"历史总计：{stats['total']} 句")
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
            if s["idx"] < self.current_idx - 1 and s["idx"] >= self.current_idx - 1 - n:
                parts.append(f"前一句: {s['chinese']}")
            elif s["idx"] > self.current_idx - 1 and s["idx"] <= self.current_idx - 1 + n:
                parts.append(f"后一句: {s['chinese']}")
        return ("上下文:\\n" + "\\n".join(parts)) if parts else ""

    def _get_subtitle_id(self, idx):
        for s in get_subtitles_for_session(self.session_id):
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
        from kivy.graphics import Color, RoundedRectangle
        content = BoxLayout(orientation='vertical', spacing=12, padding=16)
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16, 16, 16, 16])
        content.add_widget(Label(text=message, font_name='ChineseFont', font_size='15sp',
            color=(0.067, 0.078, 0.086, 1), halign='center', text_size=(300, None)))
        btn = Button(text='确定', font_name='ChineseFont', size_hint_y=None, height=44,
            background_normal='', background_color=(0.420,0.565,0.502,1), color=(1,1,1,1), font_size='15sp')
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
        popup.title_color = (0.067, 0.078, 0.086, 1)

        def _ref(inst, _):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16, 16, 16, 16])
        content.bind(pos=_ref, size=_ref)

        btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def go_home(self):
        self.manager.current = "home"

    def load_favorites_review(self, session_id, subtitles):
        self.session_id = session_id
        self.subtitles = subtitles
        self.total_count = len(subtitles)
        self.completed_count = 0
        self.current_idx = 1
        self._in_session = True
        self._update_ui_state()
        self._update_stats()
        self._show_current_sentence()