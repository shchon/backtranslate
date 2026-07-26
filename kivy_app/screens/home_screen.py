"""
Home screen - main navigation hub with stats overview.
Uxcel Go inspired design.
"""
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle

from backtranslate.database.operations import get_all_stats


# Uxcel design tokens
P = (0.486, 0.361, 1.0, 1)        # Primary #7C5CFF
P_LIGHT = (0.6, 0.5, 1.0, 0.12)   # Semi-transparent primary
BG = (1, 1, 1, 1)                  # White
CARD_BORDER = (0.91, 0.91, 0.93, 1)  # #E8E8ED
TITLE = (0, 0, 0, 1)               # #000000
HEADING = (0.102, 0.102, 0.102, 1)  # #1A1A1A
SECONDARY = (0.557, 0.557, 0.576, 1)  # #8E8E93
MUTED = (0.4, 0.4, 0.4, 1)         # #666666


class NavButton(Button):
    """Navigation card button with two-line text - Uxcel style."""
    secondary_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.font_name = 'ChineseFont'
        self.halign = 'left'
        self.valign = 'center'
        self.text_size = (self.width - 60, None)
        self.bind(size=self._update_text_size)
        self._nav_updating = False
        self.padding = [20, 0]

    def _update_text_size(self, *args):
        self.text_size = (self.width - 60, None)

    def on_secondary_text(self, *args):
        if not self._nav_updating and self.text and self.secondary_text:
            self._nav_updating = True
            self.text = f'[b]{self.text}[/b]\n[size=14][color=8E8E93]{self.secondary_text}[/color][/size]'
            self._nav_updating = False

    def on_text(self, *args):
        if not self._nav_updating and self.text and self.secondary_text:
            self._nav_updating = True
            self.text = f'[b]{self.text}[/b]\n[size=14][color=8E8E93]{self.secondary_text}[/color][/size]'
            self._nav_updating = False


Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0

        # Top status-like bar (Uxcel style)
        BoxLayout:
            size_hint_y: None
            height: 60
            padding: [20, 0]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: 'BackTranslate'
                font_name: 'ChineseFont'
                font_size: '18sp'
                bold: True
                color: 0.102, 0.102, 0.102, 1
                halign: 'left'
            Widget:
            Label:
                text: '⚡' + root.streak
                font_name: 'ChineseFont'
                font_size: '14sp'
                color: 0.4, 0.4, 0.4, 1

        # Scrollable content - Uxcel card layout
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [20, 8]
                spacing: 16

                # Streak card - Uxcel style
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 120
                    padding: [20, 16]
                    spacing: 8
                    canvas.before:
                        Color:
                            rgba: 0.486, 0.361, 1.0, 0.06
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        Line:
                            rounded_rectangle: self.pos[0], self.pos[1], self.size[0], self.size[1], 16
                            width: 0.5

                    Label:
                        text: '🔥 连续 ' + root.streak + ' 天'
                        font_name: 'ChineseFont'
                        font_size: '26sp'
                        bold: True
                        color: 0.9, 0.5, 0.13, 1
                        size_hint_y: None
                        height: 40
                    BoxLayout:
                        size_hint_y: None
                        height: 36
                        Label:
                            text: '今日 ' + root.today + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '15sp'
                            color: 0.486, 0.361, 1.0, 1
                        Label:
                            text: '总计 ' + root.total + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '15sp'
                            color: 0.4, 0.4, 0.4, 1

                # Navigation cards - Uxcel style card list
                NavButton:
                    text: '📖  开始学习'
                    secondary_text: '导入字幕，进行回译训练'
                    on_press: root.go_learn()
                NavButton:
                    text: '📊  复盘'
                    secondary_text: '查看翻译批改结果'
                    on_press: root.go_review()
                NavButton:
                    text: '⭐  收藏夹'
                    secondary_text: '管理收藏的句子'
                    on_press: root.go_favorites()
                NavButton:
                    text: '📝  表达库'
                    secondary_text: '积累的地道表达'
                    on_press: root.go_expressions()
                NavButton:
                    text: '⚙️  设置'
                    secondary_text: 'API 配置、提示词模板'
                    on_press: root.go_settings()

                # Bottom spacing
                Widget:
                    size_hint_y: None
                    height: 20


<NavButton>:
    size_hint_y: None
    height: 88
    background_normal: ''
    background_color: 1, 1, 1, 1
    font_name: 'ChineseFont'
    font_size: '17sp'
    color: 0.102, 0.102, 0.102, 1
    halign: 'left'
    valign: 'center'
    markup: True
    text_size: self.width - 60, None
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16, 16, 16, 16]
        Color:
            rgba: 0.91, 0.91, 0.93, 1
        Line:
            rounded_rectangle: self.pos[0], self.pos[1], self.size[0], self.size[1], 16
            width: 0.5
""")


class HomeScreen(Screen):
    streak = StringProperty("0")
    today = StringProperty("0")
    total = StringProperty("0")

    def on_enter(self):
        self._update_stats()

    def _update_stats(self):
        stats = get_all_stats()
        self.streak = str(stats["streak"])
        self.today = str(stats["today"])
        self.total = str(stats["total"])

    def go_learn(self):
        self.manager.current = "learn"

    def go_review(self):
        self.manager.current = "review"

    def go_favorites(self):
        self.manager.current = "favorites"

    def go_expressions(self):
        self.manager.current = "expressions"

    def go_settings(self):
        self.manager.current = "settings"