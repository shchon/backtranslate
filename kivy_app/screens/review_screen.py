"""Review screen — clean modern list layout."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

from backtranslate.database.operations import (
    get_subtitles_for_session, get_latest_translation,
    get_evaluation_for_translation, is_favorite,
    add_favorite, remove_favorite,
)
from backtranslate.database.connection import get_connection

Builder.load_string("""
<ReviewScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 0
        canvas.before:
            Color:

                rgba: 0.969, 0.973, 0.969, 1
            Rectangle:

                pos: self.pos

                size: self.size

        # ── Top bar ──
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
                text: '复盘'
                font_name: 'ChineseFont'
                font_size: '20sp'
                bold: True
                color: 0.067, 0.078, 0.086, 1
            Widget:
                size_hint_x: None
                width: 88

        Label:
            id: summary_label
            text: ''
            font_name: 'ChineseFont'
            font_size: '13sp'
            color: 0.302, 0.325, 0.349, 1
            size_hint_y: None
            height: 36
            padding: [20, 8]

        ScrollView:
            id: scroll_view
            BoxLayout:
                id: list_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [16, 4]
                spacing: 10
""")


class ReviewScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.session_id = None
        self.subtitle_rows = []
        self.only_translated = False

    def on_enter(self):
        if self.session_id:
            self.load_session(self.session_id, self.only_translated)

    def load_session(self, session_id, only_translated=False):
        self.session_id = session_id
        self.only_translated = only_translated
        self.subtitle_rows = get_subtitles_for_session(session_id)
        self._refresh_list()

    def update_evaluation(self, subtitle_id):
        self._refresh_list()

    def _refresh_list(self):
        layout = self.ids.list_layout
        layout.clear_widgets()
        completed = 0
        visible = 0

        for sub in self.subtitle_rows:
            if self.only_translated and not self._get_latest_translation_id(sub["id"]):
                continue
            visible += 1
            ev = self._get_latest_eval(sub["id"])
            if ev and ev["status"] == "done":
                completed += 1

            card = BoxLayout(orientation='vertical', size_hint_y=None,
                             height=200, padding=[16, 12], spacing=4)
            with card.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=card.pos, size=card.size, radius=[16]*4)

            def update_bg(inst, val):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(rgba=(1, 1, 1, 1))
                    RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16]*4)
            card.bind(pos=update_bg, size=update_bg)

            # Header row
            hdr = BoxLayout(size_hint_y=None, height=30, spacing=8)
            hdr.add_widget(Label(text=f"#{sub['idx']}", font_name='ChineseFont',
                font_size='12sp', color=(0.420, 0.447, 0.475, 1), size_hint_x=None, width=32))
            hdr.add_widget(Label(text=sub['chinese'], font_name='ChineseFont',
                font_size='16sp', color=(0.067, 0.078, 0.086, 1),
                halign='left'))
            hdr.add_widget(Widget(size_hint_x=1))

            # Status badge
            if not ev or ev["status"] == "pending":
                st = Label(text='⏳ 等待', font_name='ChineseFont', font_size='11sp',
                    color=(0.420, 0.447, 0.475, 1), size_hint_x=None, width=54)
            elif ev["status"] == "processing":
                st = Label(text='🔄 批改中', font_name='ChineseFont', font_size='11sp',
                    color=(0.925, 0.596, 0.235, 1), size_hint_x=None, width=54)
            elif ev["status"] == "failed":
                st = Label(text='❌ 失败', font_name='ChineseFont', font_size='11sp',
                    color=(0.878, 0.345, 0.298, 1), size_hint_x=None, width=54)
            else:
                a = (ev["meaning_score"]+ev["grammar_score"]+ev["naturalness_score"]+ev["subtitle_style_score"])/4
                c = (0.357,0.620,0.490,1) if a>=80 else (0.925,0.596,0.235,1) if a>=60 else (0.878,0.345,0.298,1)
                st = Label(text=f'{a:.0f}', font_name='ChineseFont', font_size='14sp', bold=True,
                    color=c, size_hint_x=None, width=44)
            hdr.add_widget(st)

            # Fav star
            is_fav = is_favorite(sub['id'])
            fbtn = Button(text='★' if is_fav else '☆', font_size='22sp',
                size_hint_x=None, width=40,
                background_normal='', background_color=(0,0,0,0),
                color=(0.925,0.596,0.235,1) if is_fav else (0.420,0.447,0.475,1))
            fbtn.subtitle_id = sub['id']
            fbtn.bind(on_press=self._on_fav_toggle)
            hdr.add_widget(fbtn)
            card.add_widget(hdr)

            # User translation
            ut = get_latest_translation(sub["id"])
            if ut:
                card.add_widget(Label(text=f'你的翻译: {ut}', font_name='ChineseFont',
                    font_size='14sp', color=(0.376,0.533,0.820,1),
                    size_hint_y=None, height=22, halign='left'))

            # Scores
            if ev and ev["status"] == "done":
                sr = BoxLayout(size_hint_y=None, height=24, spacing=6)
                for n, k in [("意思","meaning_score"),("语法","grammar_score"),
                             ("自然","naturalness_score"),("字幕","subtitle_style_score")]:
                    s = ev[k]
                    c = (0.357,0.620,0.490,1) if s>=80 else (0.925,0.596,0.235,1) if s>=60 else (0.878,0.345,0.298,1)
                    sr.add_widget(Label(text=f'{n} {s}', font_name='ChineseFont',
                        font_size='11sp', color=c, size_hint_x=None, width=64))
                sr.add_widget(Widget())
                card.add_widget(sr)

            # Expand
            xbtn = Button(text='查看详情 ›', font_size='13sp',
                color=(0.420, 0.565, 0.502, 1),
                size_hint_y=None, height=28,
                background_normal='', background_color=(0,0,0,0))
            xbtn.eval_data = ev
            xbtn.sub = sub
            xbtn.bind(on_press=self._show_detail)
            card.add_widget(xbtn)
            layout.add_widget(card)

        total = len(self.subtitle_rows)
        if self.only_translated:
            self.ids.summary_label.text = f"已翻译 {visible} 句 · 已批改 {completed} · 共 {total} 句"
        else:
            self.ids.summary_label.text = f"共 {total} 句 · 已批改 {completed} 句"

        if not layout.children:
            layout.add_widget(Label(text='暂无数据', font_name='ChineseFont',
                font_size='15sp', color=(0.302,0.325,0.349,1), size_hint_y=None, height=200))

    def _on_fav_toggle(self, btn):
        sid = btn.subtitle_id
        if is_favorite(sid):
            remove_favorite(sid)
            btn.text = '☆'
            btn.color = (0.420, 0.447, 0.475, 1)
        else:
            add_favorite(sid)
            btn.text = '★'
            btn.color = (0.925, 0.596, 0.235, 1)

    def _show_detail(self, btn):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView

        sub = btn.sub
        ev = btn.eval_data
        from kivy.graphics import Color, RoundedRectangle
        content = BoxLayout(orientation='vertical', spacing=10, padding=16)
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16]*4)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(content)

        popup = Popup(title=f'#{sub["idx"]} 详情', content=scroll,
                      size_hint=(0.9, 0.85), auto_dismiss=True)
        popup.title_color = (0.067, 0.078, 0.086, 1)

        def _ref(inst, _):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16]*4)
        content.bind(pos=_ref, size=_ref)

        content.add_widget(Label(text=sub['chinese'], font_name='ChineseFont',
            font_size='18sp', bold=True, color=(0.067,0.078,0.086,1),
            size_hint_y=None, height=50, text_size=(320,None), halign='left'))

        ut = get_latest_translation(sub["id"])
        if ut:
            content.add_widget(Label(text=f'你的翻译: {ut}', font_name='ChineseFont',
                font_size='14sp', color=(0.376,0.533,0.820,1),
                size_hint_y=None, height=26))

        if ev and ev["status"] == "done" and ev.get("analysis_text"):
            al = Label(text=ev["analysis_text"], font_name='ChineseFont',
                font_size='14sp', color=(0.067,0.078,0.086,1),
                size_hint_y=None, height=80, text_size=(320,None), halign='left')
            al.bind(texture_size=lambda inst, val: setattr(inst, 'height', max(60,val[1])))
            content.add_widget(al)

        # Official
        obtn = Button(text='查看官方字幕 ▸', font_size='13sp',
            color=(0.420,0.565,0.502,1), size_hint_y=None, height=32,
            background_normal='', background_color=(0,0,0,0))
        ol = Label(text=sub['english_official'], font_name='ChineseFont',
            font_size='14sp', color=(0.302,0.325,0.349,1),
            size_hint_y=None, height=26, opacity=0, disabled=True,
            text_size=(320,None))
        def toggle(o):
            ol.opacity = 1 - ol.opacity
            ol.disabled = not ol.disabled
            o.text = '隐藏 ▾' if ol.opacity else '查看官方字幕 ▸'
        obtn.bind(on_press=toggle)
        content.add_widget(obtn)
        content.add_widget(ol)

        # Redo
        ri = TextInput(hint_text='重新翻译……', font_name='ChineseFont',
            font_size='15sp', size_hint_y=None, height=40, multiline=False,
            background_color=(0.890,0.898,0.886,1), foreground_color=(0.067,0.078,0.086,1),
            padding=[14,10])
        rb = Button(text='提交重新翻译', font_name='ChineseFont', font_size='15sp', bold=True,
            size_hint_y=None, height=44,
            background_normal='', background_color=(0.420,0.565,0.502,1), color=(1,1,1,1))
        def redo(b):
            t = ri.text.strip()
            if not t:
                return
            from backtranslate.database.operations import create_translation, create_evaluation
            c = get_connection()
            r = c.execute("SELECT MAX(version) FROM translations WHERE subtitle_id=?",
                          (sub["id"],)).fetchone()
            c.close()
            v = (r[0] or 0) + 1
            tid = create_translation(sub["id"], t, v)
            eid = create_evaluation(tid)
            from kivy.app import App
            app = App.get_running_app()
            if app and app.worker:
                app.worker.add_task(eid, 0, t, sub["english_official"],
                                    self._build_context(sub))
            popup.dismiss()
        rb.bind(on_press=redo)
        content.add_widget(ri)
        content.add_widget(rb)

        cb = Button(text='关闭', font_name='ChineseFont', font_size='15sp',
            size_hint_y=None, height=44,
            background_normal='', background_color=(0.890,0.898,0.886,1),
            color=(0.302,0.325,0.349,1))
        cb.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(cb)
        popup.open()

    def _build_context(self, sub):
        from backtranslate.config import load_config
        n = load_config().get("context_n", 1)
        if n == 0:
            return ""
        parts = []
        for s in self.subtitle_rows:
            if s["idx"] < sub["idx"] and s["idx"] >= sub["idx"] - n:
                parts.append(f"前一句: {s['chinese']}")
            elif s["idx"] > sub["idx"] and s["idx"] <= sub["idx"] + n:
                parts.append(f"后一句: {s['chinese']}")
        return ("上下文:\
" + "\
".join(parts)) if parts else ""

    def _get_latest_eval(self, sid):
        tid = self._get_latest_translation_id(sid)
        return get_evaluation_for_translation(tid) if tid else None

    def _get_latest_translation_id(self, sid):
        c = get_connection()
        r = c.execute("SELECT id FROM translations WHERE subtitle_id=? ORDER BY version DESC LIMIT 1",
                      (sid,)).fetchone()
        c.close()
        return r[0] if r else None

    def go_home(self):
        self.manager.current = "home"
