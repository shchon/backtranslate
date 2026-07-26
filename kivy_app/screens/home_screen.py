"""Home screen — clean modern card-flow with full-width touch targets."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from backtranslate.database.operations import get_all_stats


class CardRow(ButtonBehavior, BoxLayout):
    """A tappable card row — the entire card area responds to touch."""
    pass


# Color tokens — consistent with main.py
PRI     = (0.420, 0.565, 0.502, 1)   # #6B9080  primary
WHITE   = (1, 1, 1, 1)
TX1     = (0.067, 0.078, 0.086, 1)   # #111416  text primary
TX2     = (0.302, 0.325, 0.349, 1)   # #4D5359  text secondary
TX3     = (0.420, 0.447, 0.475, 1)   # #6B7279  text muted
SURFACE = (0.890, 0.898, 0.886, 1)    # #E3E5E2

Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 0
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
            padding: [20, 0]
            Label:
                text: '你好 👋'
                font_name: 'ChineseFont'
                font_size: '24sp'
                bold: True
                color: 0.067, 0.078, 0.086, 1
                halign: 'left'
            Widget:
            Label:
                text: '🔥 ' + root.streak + ' 天'
                font_name: 'ChineseFont'
                font_size: '14sp'
                color: 0.302, 0.325, 0.349, 1
                size_hint_x: None
                width: 120
                halign: 'right'

        # ── Scroll ──
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [16, 8]
                spacing: 12

                # ── Stats card ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 150
                    padding: [20, 18]
                    spacing: 8

                    Label:
                        text: '今日学习'
                        font_name: 'ChineseFont'
                        font_size: '15sp'
                        color: 0.302, 0.325, 0.349, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'
                    Label:
                        text: root.today + ' 句'
                        font_name: 'ChineseFont'
                        font_size: '36sp'
                        bold: True
                        color: 0.420, 0.565, 0.502, 1
                        size_hint_y: None
                        height: 44
                        halign: 'left'
                    BoxLayout:
                        size_hint_y: None
                        height: 22
                        spacing: 16
                        Label:
                            text: '总计 ' + root.total + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '14sp'
                            color: 0.302, 0.325, 0.349, 1
                            size_hint_x: None
                            width: 140
                            halign: 'left'

                # ── Section ──
                Label:
                    text: '学习工具'
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    bold: True
                    color: 0.302, 0.325, 0.349, 1
                    size_hint_y: None
                    height: 32
                    halign: 'left'
                    padding: [12, 0]

                # ── Card 1 : 学习 (full-width tappable) ──
                CardRow:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]

                    on_release: root.go_learn()
                    Widget:
                        size_hint_x: None
                        width: 48
                        Label:
                            text: '📖'
                            font_size: '24sp'
                            size_hint_x: None
                            width: 48
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        padding: [0, 14]
                        spacing: 2
                        Label:
                            text: '回译学习'
                            font_name: 'ChineseFont'
                            font_size: '17sp'
                            bold: True
                            color: 0.067, 0.078, 0.086, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '导入字幕 · 中英回译训练'
                            font_name: 'ChineseFont'
                            font_size: '13sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Widget:
                        size_hint_x: None
                        width: 36
                        Label:
                            text: '›'
                            font_size: '22sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_x: None
                            width: 36

                # ── Card 2 : 复盘 ──
                CardRow:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]

                    on_release: root.go_review()
                    Widget:
                        size_hint_x: None
                        width: 48
                        Label:
                            text: '📊'
                            font_size: '24sp'
                            size_hint_x: None
                            width: 48
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        padding: [0, 14]
                        spacing: 2
                        Label:
                            text: '复盘回顾'
                            font_name: 'ChineseFont'
                            font_size: '17sp'
                            bold: True
                            color: 0.067, 0.078, 0.086, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '查看 AI 批改结果与评分'
                            font_name: 'ChineseFont'
                            font_size: '13sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Widget:
                        size_hint_x: None
                        width: 36
                        Label:
                            text: '›'
                            font_size: '22sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_x: None
                            width: 36

                # ── Card 3 : 收藏 ──
                CardRow:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]

                    on_release: root.go_favorites()
                    Widget:
                        size_hint_x: None
                        width: 48
                        Label:
                            text: '⭐'
                            font_size: '24sp'
                            size_hint_x: None
                            width: 48
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        padding: [0, 14]
                        spacing: 2
                        Label:
                            text: '收藏夹'
                            font_name: 'ChineseFont'
                            font_size: '17sp'
                            bold: True
                            color: 0.067, 0.078, 0.086, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '管理收藏的句子'
                            font_name: 'ChineseFont'
                            font_size: '13sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Widget:
                        size_hint_x: None
                        width: 36
                        Label:
                            text: '›'
                            font_size: '22sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_x: None
                            width: 36

                # ── Card 4 : 表达库 ──
                CardRow:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]

                    on_release: root.go_expressions()
                    Widget:
                        size_hint_x: None
                        width: 48
                        Label:
                            text: '📝'
                            font_size: '24sp'
                            size_hint_x: None
                            width: 48
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        padding: [0, 14]
                        spacing: 2
                        Label:
                            text: '表达库'
                            font_name: 'ChineseFont'
                            font_size: '17sp'
                            bold: True
                            color: 0.067, 0.078, 0.086, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: 'AI 推荐的地道英文表达'
                            font_name: 'ChineseFont'
                            font_size: '13sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Widget:
                        size_hint_x: None
                        width: 36
                        Label:
                            text: '›'
                            font_size: '22sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_x: None
                            width: 36

                # ── Card 5 : 设置 ──
                CardRow:
                    size_hint_y: None
                    height: 60
                    padding: [20, 0]

                    on_release: root.go_settings()
                    Widget:
                        size_hint_x: None
                        width: 48
                        Label:
                            text: '⚙️'
                            font_size: '22sp'
                            size_hint_x: None
                            width: 48
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        padding: [0, 10]
                        spacing: 2
                        Label:
                            text: '设置'
                            font_name: 'ChineseFont'
                            font_size: '17sp'
                            color: 0.067, 0.078, 0.086, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                    Widget:
                        size_hint_x: None
                        width: 36
                        Label:
                            text: '›'
                            font_size: '22sp'
                            color: 0.420, 0.447, 0.475, 1
                            size_hint_x: None
                            width: 36

                Widget:
                    size_hint_y: None
                    height: 32
""")


class HomeScreen(Screen):
    streak = StringProperty("0")
    today = StringProperty("0")
    total = StringProperty("0")

    def on_enter(self):
        s = get_all_stats()
        self.streak = str(s["streak"])
        self.today = str(s["today"])
        self.total = str(s["total"])

    def go_learn(self, *a):
        self.manager.current = "learn"
    def go_review(self, *a):
        self.manager.current = "review"
    def go_favorites(self, *a):
        self.manager.current = "favorites"
    def go_expressions(self, *a):
        self.manager.current = "expressions"
    def go_settings(self, *a):
        self.manager.current = "settings"
