"""
Home screen - KakaoBank inspired design.
4 colored feature cards + banner + stats.
"""
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

from backtranslate.database.operations import get_all_stats

# KakaoBank tokens
MINT   = (0.776, 0.894, 0.827, 1)     # #C6E4D3
ORANGE = (0.953, 0.490, 0.369, 1)     # #F37D5E
BLUE   = (0.318, 0.529, 0.651, 1)     # #5187A6
KHAKI  = (0.788, 0.761, 0.682, 1)     # #C9C2AE

MINT_L   = (0.839, 0.906, 0.867, 1)   # #D6E7DD
ORANGE_L = (0.973, 0.686, 0.561, 1)   # #F8AF8F
BLUE_L   = (0.569, 0.694, 0.769, 1)   # #91B1C4
KHAKI_L  = (0.871, 0.851, 0.780, 1)   # #DED9C7

BG    = (0.965, 0.965, 0.965, 1)     # #F6F6F6
WHITE = (1, 1, 1, 1)
TITLE     = (0.067, 0.067, 0.067, 1)   # #111111
BODY      = (0.165, 0.165, 0.165, 1)   # #2A2A2A
SECONDARY = (0.533, 0.533, 0.533, 1)   # #888888
SEP       = (0.886, 0.914, 0.898, 1)   # #E2E9E5

Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        canvas.before:
            Color:
                rgba: 0.965, 0.965, 0.965, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # ── Top bar (56dp, same bg as page) ──
        BoxLayout:
            size_hint_y: None
            height: 56
            padding: [20, 0]
            canvas.before:
                Color:
                    rgba: 0.965, 0.965, 0.965, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: '你好 👋'
                font_name: 'ChineseFont'
                font_size: '18sp'
                bold: True
                color: 0.067, 0.067, 0.067, 1
                halign: 'left'
            Widget:
            Label:
                text: '🔥 连续 ' + root.streak + ' 天'
                font_name: 'ChineseFont'
                font_size: '13sp'
                color: 0.533, 0.533, 0.533, 1
                size_hint_x: None
                width: 150
                halign: 'right'

        # ── Scrollable content ──
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [16, 8]
                spacing: 16

                # ── Stats overview card (white) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 140
                    padding: [24, 20]
                    spacing: 12
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        text: '今日学习'
                        font_name: 'ChineseFont'
                        font_size: '16sp'
                        color: 0.533, 0.533, 0.533, 1
                        size_hint_y: None
                        height: 22
                        halign: 'left'
                    Label:
                        text: root.today + ' 句'
                        font_name: 'ChineseFont'
                        font_size: '36sp'
                        bold: True
                        color: 0.067, 0.067, 0.067, 1
                        size_hint_y: None
                        height: 44
                        halign: 'left'
                    BoxLayout:
                        size_hint_y: None
                        height: 20
                        spacing: 4
                        Label:
                            text: '总计 ' + root.total + ' 句'
                            font_name: 'ChineseFont'
                            font_size: '14sp'
                            color: 0.533, 0.533, 0.533, 1
                            size_hint_x: None
                            width: 150
                            halign: 'left'

                # ── Feature card 1: 学习 (mint) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 170
                    padding: [24, 20]
                    spacing: 10
                    canvas.before:
                        Color:
                            rgba: 0.776, 0.894, 0.827, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        text: '📖  回译学习'
                        font_name: 'ChineseFont'
                        font_size: '20sp'
                        bold: True
                        color: 0.067, 0.067, 0.067, 1
                        size_hint_y: None
                        height: 28
                        halign: 'left'
                    Label:
                        text: '导入字幕进行中英回译训练'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.165, 0.165, 0.165, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'
                    Widget:
                    BoxLayout:
                        size_hint_y: None
                        height: 48
                        spacing: 12
                        Button:
                            text: '开始'
                            font_name: 'ChineseFont'
                            font_size: '16sp'
                            bold: True
                            color: 0.067, 0.067, 0.067, 1
                            background_normal: ''
                            background_color: 0.839, 0.906, 0.867, 1
                            on_press: root.go_learn()
                            canvas.before:
                                Color:
                                    rgba: 0.839, 0.906, 0.867, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [20, 20, 20, 20]
                        Widget:

                # ── Feature card 2: 复习 (orange) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 170
                    padding: [24, 20]
                    spacing: 10
                    canvas.before:
                        Color:
                            rgba: 0.953, 0.490, 0.369, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        text: '📊  复盘回顾'
                        font_name: 'ChineseFont'
                        font_size: '20sp'
                        bold: True
                        color: 1, 1, 1, 1
                        size_hint_y: None
                        height: 28
                        halign: 'left'
                    Label:
                        text: '查看 AI 批改结果和评分'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.973, 0.906, 0.875, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'
                    Widget:
                    BoxLayout:
                        size_hint_y: None
                        height: 48
                        spacing: 12
                        Button:
                            text: '查看'
                            font_name: 'ChineseFont'
                            font_size: '16sp'
                            bold: True
                            color: 1, 1, 1, 1
                            background_normal: ''
                            background_color: 0.973, 0.686, 0.561, 1
                            on_press: root.go_review()
                            canvas.before:
                                Color:
                                    rgba: 0.973, 0.686, 0.561, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [20, 20, 20, 20]
                        Widget:

                # ── Feature card 3: 表达库 (blue) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 170
                    padding: [24, 20]
                    spacing: 10
                    canvas.before:
                        Color:
                            rgba: 0.318, 0.529, 0.651, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        text: '📝  表达库'
                        font_name: 'ChineseFont'
                        font_size: '20sp'
                        bold: True
                        color: 1, 1, 1, 1
                        size_hint_y: None
                        height: 28
                        halign: 'left'
                    Label:
                        text: 'AI 推荐的地道英文表达'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.875, 0.875, 0.875, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'
                    Widget:
                    BoxLayout:
                        size_hint_y: None
                        height: 48
                        spacing: 12
                        Button:
                            text: '浏览'
                            font_name: 'ChineseFont'
                            font_size: '16sp'
                            bold: True
                            color: 1, 1, 1, 1
                            background_normal: ''
                            background_color: 0.569, 0.694, 0.769, 1
                            on_press: root.go_expressions()
                            canvas.before:
                                Color:
                                    rgba: 0.569, 0.694, 0.769, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [20, 20, 20, 20]
                        Widget:

                # ── Feature card 4: 收藏 (khaki) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 170
                    padding: [24, 20]
                    spacing: 10
                    canvas.before:
                        Color:
                            rgba: 0.788, 0.761, 0.682, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Label:
                        text: '⭐  收藏夹'
                        font_name: 'ChineseFont'
                        font_size: '20sp'
                        bold: True
                        color: 1, 1, 1, 1
                        size_hint_y: None
                        height: 28
                        halign: 'left'
                    Label:
                        text: '管理收藏的句子'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.91, 0.91, 0.91, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'
                    Widget:
                    BoxLayout:
                        size_hint_y: None
                        height: 48
                        spacing: 12
                        Button:
                            text: '查看'
                            font_name: 'ChineseFont'
                            font_size: '16sp'
                            bold: True
                            color: 1, 1, 1, 1
                            background_normal: ''
                            background_color: 0.871, 0.851, 0.780, 1
                            on_press: root.go_favorites()
                            canvas.before:
                                Color:
                                    rgba: 0.871, 0.851, 0.780, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [20, 20, 20, 20]
                        Widget:

                # ── Settings card (subtle) ──
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 90
                    padding: [24, 20]
                    spacing: 6
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [28, 28, 28, 28]
                    Button:
                        text: '⚙️  设置'
                        font_name: 'ChineseFont'
                        font_size: '18sp'
                        color: 0.067, 0.067, 0.067, 1
                        background_normal: ''
                        background_color: 0, 0, 0, 0
                        size_hint_y: None
                        height: 30
                        halign: 'left'
                        valign: 'middle'
                        on_press: root.go_settings()

                # Bottom
                Widget:
                    size_hint_y: None
                    height: 20
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
