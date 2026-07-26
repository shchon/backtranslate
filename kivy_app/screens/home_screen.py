"""Home screen — clean modern card-flow layout."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from backtranslate.database.operations import get_all_stats

# Design tokens (sync with main.py)
PRI = (0.420, 0.565, 0.502, 1)   # #6B9080
P_L = (0.910, 0.941, 0.925, 1)   # #E8F0EC
WHITE = (1, 1, 1, 1)
T1 = (0.102, 0.110, 0.118, 1)    # #1A1C1E
T2 = (0.408, 0.439, 0.471, 1)    # #687078
T3 = (0.616, 0.643, 0.667, 1)    # #9DA4AA
BORDER = (0.902, 0.910, 0.902, 1)  # #E6E8E6
RAD = 16

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
            canvas.before:
                Color:

                    rgba: 0.969, 0.973, 0.969, 1
                Rectangle:

                    pos: self.pos

                    size: self.size
            Label:
                text: '你好 👋'
                font_name: 'ChineseFont'
                font_size: '24sp'
                bold: True
                color: 0.102, 0.110, 0.118, 1
                halign: 'left'
            Widget:
            Label:
                text: '🔥 ' + root.streak + ' 天'
                font_name: 'ChineseFont'
                font_size: '13sp'
                color: 0.408, 0.439, 0.471, 1
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
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
                    Label:
                        text: '今日学习'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.408, 0.439, 0.471, 1
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
                        height: 20
                        spacing: 16
                        Label:
                            text: '总计 ' + root.total + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '13sp'
                            color: 0.616, 0.643, 0.667, 1
                            size_hint_x: None
                            width: 140
                            halign: 'left'

                # ── Section label ──
                Label:
                    text: '学习工具'
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    bold: True
                    color: 0.408, 0.439, 0.471, 1
                    size_hint_y: None
                    height: 32
                    halign: 'left'
                    padding: [12, 0]

                # ── Card 1 : 学习 ──
                BoxLayout:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
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
                            color: 0.102, 0.110, 0.118, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '导入字幕 · 中英回译训练'
                            font_name: 'ChineseFont'
                            font_size: '12sp'
                            color: 0.616, 0.643, 0.667, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Button:
                        text: '›'
                        font_size: '22sp'
                        color: 0.616, 0.643, 0.667, 1
                        size_hint_x: None
                        width: 36
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        on_press: root.go_learn()

                # ── Card 2 : 复盘 ──
                BoxLayout:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
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
                            color: 0.102, 0.110, 0.118, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '查看 AI 批改结果与评分'
                            font_name: 'ChineseFont'
                            font_size: '12sp'
                            color: 0.616, 0.643, 0.667, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Button:
                        text: '›'
                        font_size: '22sp'
                        color: 0.616, 0.643, 0.667, 1
                        size_hint_x: None
                        width: 36
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        on_press: root.go_review()

                # ── Card 3 : 收藏 ──
                BoxLayout:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
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
                            color: 0.102, 0.110, 0.118, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: '管理收藏的句子'
                            font_name: 'ChineseFont'
                            font_size: '12sp'
                            color: 0.616, 0.643, 0.667, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Button:
                        text: '›'
                        font_size: '22sp'
                        color: 0.616, 0.643, 0.667, 1
                        size_hint_x: None
                        width: 36
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        on_press: root.go_favorites()

                # ── Card 4 : 表达库 ──
                BoxLayout:
                    size_hint_y: None
                    height: 72
                    padding: [20, 0]
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
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
                            color: 0.102, 0.110, 0.118, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                        Label:
                            text: 'AI 推荐的地道英文表达'
                            font_name: 'ChineseFont'
                            font_size: '12sp'
                            color: 0.616, 0.643, 0.667, 1
                            size_hint_y: None
                            height: 16
                            halign: 'left'
                    Button:
                        text: '›'
                        font_size: '22sp'
                        color: 0.616, 0.643, 0.667, 1
                        size_hint_x: None
                        width: 36
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        on_press: root.go_expressions()

                # ── Card 5 : 设置 ──
                BoxLayout:
                    size_hint_y: None
                    height: 60
                    padding: [20, 0]
                    canvas.before:
                        Color:

                            rgba: 1, 1, 1, 1
                        RoundedRectangle:

                            pos: self.pos

                            size: self.size

                            radius: [16]*4
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
                            font_size: '16sp'
                            color: 0.102, 0.110, 0.118, 1
                            size_hint_y: None
                            height: 24
                            halign: 'left'
                    Button:
                        text: '›'
                        font_size: '22sp'
                        color: 0.616, 0.643, 0.667, 1
                        size_hint_x: None
                        width: 36
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        on_press: root.go_settings()

                # ── Bottom spacer ──
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
