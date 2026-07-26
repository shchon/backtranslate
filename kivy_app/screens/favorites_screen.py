"""Favorites screen — clean modern card list."""
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

from backtranslate.database.operations import (
    get_favorites, remove_favorite, clear_favorites, is_favorite,
    add_favorite, create_session, create_subtitles_batch,
    get_subtitles_for_session,
)
from backtranslate.database.connection import init_db

Builder.load_string("""
<FavoritesScreen>:
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
                text: '收藏夹'
                font_name: 'ChineseFont'
                font_size: '20sp'
                bold: True
                color: 0.102, 0.110, 0.118, 1
            Button:
                text: '复习'
                size_hint_x: None
                width: 52
                background_normal: ''
                background_color: 0,0,0,0
                color: 0.420, 0.565, 0.502, 1
                font_name: 'ChineseFont'
                font_size: '15sp'
                on_press: root.start_review()
            Button:
                text: '清空'
                size_hint_x: None
                width: 52
                background_normal: ''
                background_color: 0,0,0,0
                color: 0.878, 0.345, 0.298, 1
                font_name: 'ChineseFont'
                font_size: '15sp'
                on_press: root.clear_all()

        Label:
            id: count_label
            text: ''
            font_name: 'ChineseFont'
            font_size: '13sp'
            color: 0.408, 0.439, 0.471, 1
            size_hint_y: None
            height: 32
            padding: [20, 8]

        ScrollView:
            BoxLayout:
                id: list_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [16, 4]
                spacing: 8
""")


class FavoritesScreen(Screen):
    def on_enter(self):
        self._refresh()

    def _refresh(self):
        layout = self.ids.list_layout
        layout.clear_widgets()
        favs = get_favorites()
        self.ids.count_label.text = f"共 {len(favs)} 句"

        if not favs:
            layout.add_widget(Label(text='暂无收藏句子', font_name='ChineseFont',
                font_size='15sp', color=(0.408,0.439,0.471,1), size_hint_y=None, height=200))
            return

        for i, f in enumerate(favs):
            card = BoxLayout(orientation='vertical', size_hint_y=None,
                            height=100, padding=[16, 12], spacing=4)
            with card.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=card.pos, size=card.size, radius=[16]*4)

            def update_bg(inst, val):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(rgba=(1, 1, 1, 1))
                    RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16]*4)
            card.bind(pos=update_bg, size=update_bg)

            row = BoxLayout(size_hint_y=None, height=36, spacing=8)
            row.add_widget(Label(text=f"#{i+1}", font_name='ChineseFont',
                font_size='12sp', color=(0.616,0.643,0.667,1), size_hint_x=None, width=32))
            row.add_widget(Label(text=f["chinese"], font_name='ChineseFont',
                font_size='16sp', color=(0.102,0.110,0.118,1), halign='left'))
            db = Button(text='×', font_size='20sp', color=(0.878,0.345,0.298,1),
                size_hint_x=None, width=36, background_normal='', background_color=(0,0,0,0))
            db.fav_id = f["id"]
            db.bind(on_press=self._delete)
            row.add_widget(db)
            card.add_widget(row)

            # English toggle
            eb = Button(text='查看英文 ▸', font_name='ChineseFont', font_size='13sp',
                color=(0.420,0.565,0.502,1), size_hint_y=None, height=24,
                background_normal='', background_color=(0,0,0,0), halign='left')
            el = Label(text=f["english_official"], font_name='ChineseFont',
                font_size='14sp', color=(0.408,0.439,0.471,1),
                size_hint_y=None, height=22, opacity=0, disabled=True,
                text_size=(self.width-40,None))
            def toggle_en(b, l=el):
                l.opacity = 1 - l.opacity
                l.disabled = not l.disabled
                b.text = '隐藏 ▾' if l.opacity else '查看英文 ▸'
            eb.bind(on_press=toggle_en)
            card.add_widget(eb)
            card.add_widget(el)
            layout.add_widget(card)

    def _delete(self, btn):
        remove_favorite(btn.fav_id)
        self._refresh()

    def start_review(self):
        favs = get_favorites()
        if not favs:
            self._toast('收藏夹为空')
            return
        init_db()
        from backtranslate.database.operations import clear_session_data
        clear_session_data()
        sid = create_session("收藏复习", len(favs))
        subs = []
        for i, f in enumerate(favs):
            subs.append({"idx": i+1, "chinese": f["chinese"], "english_official": f["english_official"]})
        create_subtitles_batch(sid, subs)
        db_subs = get_subtitles_for_session(sid)
        self.manager.get_screen("learn").load_favorites_review(sid, db_subs)
        self.manager.current = "learn"

    def clear_all(self):
        content = BoxLayout(orientation='vertical', spacing=12, padding=16)
        content.add_widget(Label(text='确定清空所有收藏？', font_name='ChineseFont',
            font_size='15sp', color=(0.102,0.110,0.118,1), halign='center'))
        btns = BoxLayout(size_hint_y=None, height=44, spacing=12)
        cb = Button(text='取消', font_name='ChineseFont', font_size='15sp',
            background_normal='', background_color=(0.953,0.957,0.953,1),
            color=(0.408,0.439,0.471,1))
        ok = Button(text='清空', font_name='ChineseFont', font_size='15sp', bold=True,
            background_normal='', background_color=(0.878,0.345,0.298,1), color=(1,1,1,1))
        btns.add_widget(cb)
        btns.add_widget(ok)
        content.add_widget(btns)
        popup = Popup(title='确认', content=content, size_hint=(0.8,0.35), auto_dismiss=False)
        cb.bind(on_press=lambda x: popup.dismiss())
        ok.bind(on_press=lambda x: [clear_favorites(), popup.dismiss(), self._refresh()])
        popup.open()

    def _toast(self, msg):
        popup = Popup(title='', content=Label(text=msg, font_name='ChineseFont',
            font_size='15sp', color=(0.102,0.110,0.118,1)),
            size_hint=(0.7,0.2), auto_dismiss=True)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def go_home(self):
        self.manager.current = "home"
