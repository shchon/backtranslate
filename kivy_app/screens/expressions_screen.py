"""Expressions screen — clean modern search + list."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

from backtranslate.database.operations import get_all_expressions, delete_expression

Builder.load_string("""
<ExpressionsScreen>:
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
                font_size: '9sp'
                on_press: root.go_home()
            Label:
                text: '表达库'
                font_name: 'ChineseFont'
                font_size: '13sp'
                bold: True
                color: 0.067, 0.078, 0.086, 1
            Widget:
                size_hint_x: None
                width: 88

        # Search
        TextInput:
            id: search_input
            hint_text: '🔍 搜索表达……'
            hint_text_color: 0.420, 0.447, 0.475, 1
            font_name: 'ChineseFont'
            font_size: '8sp'
            size_hint_y: None
            height: 44
            padding: [16, 12]
            multiline: False
            background_color: 1, 1, 1, 1
            foreground_color: 0, 0, 0, 1
            on_text: root._refresh()

        ScrollView:
            BoxLayout:
                id: list_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [16, 8]
                spacing: 8
""")


class ExpressionsScreen(Screen):
    def on_enter(self):
        self._refresh()

    def _refresh(self):
        layout = self.ids.list_layout
        layout.clear_widgets()
        expressions = get_all_expressions()
        q = self.ids.search_input.text.strip().lower()

        for expr in expressions:
            if q and q not in expr["phrase"].lower():
                continue
            card = BoxLayout(orientation='vertical', size_hint_y=None,
                            height=52, padding=[16, 12], spacing=4)
            with card.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=card.pos, size=card.size, radius=[16]*4)

            def update_bg(inst, val):
                inst.canvas.before.clear()
                with inst.canvas.before:
                    Color(rgba=(1, 1, 1, 1))
                    RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16]*4)
            card.bind(pos=update_bg, size=update_bg)

            row = BoxLayout(size_hint_y=None, height=32, spacing=8)
            row.add_widget(Label(text=expr["phrase"], font_name='ChineseFont',
                font_size='9sp', bold=True, color=(0.102,0.110,0.118,1), halign='left'))
            db = Button(text='删除', font_name='ChineseFont', font_size='8sp',
                color=(0.878,0.345,0.298,1), size_hint_x=None, width=48,
                background_normal='', background_color=(0,0,0,0))
            db.expr_id = expr["id"]
            db.bind(on_press=self._delete)
            row.add_widget(db)
            card.add_widget(row)
            layout.add_widget(card)

        if not layout.children:
            layout.add_widget(Label(text='还没有收藏的表达', font_name='ChineseFont',
                font_size='8sp', color=(0.408,0.439,0.471,1), size_hint_y=None, height=200))

    def _delete(self, btn):
        delete_expression(btn.expr_id)
        self._refresh()

    def go_home(self):
        self.manager.current = "home"
