"""Home screen — clean card-flow layout with standard Button cards."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from backtranslate.database.operations import get_all_stats

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
                    height: 130
                    padding: [20, 16]
                    spacing: 4
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]
                    Label:
                        text: '今日学习'
                        font_name: 'ChineseFont'
                        font_size: '15sp'
                        color: 0.302, 0.325, 0.349, 1
                        size_hint_y: None
                        height: 22
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
                    Label:
                        text: '总计 ' + root.total + ' 句'
                        font_name: 'ChineseFont'
                        font_size: '14sp'
                        color: 0.302, 0.325, 0.349, 1
                        size_hint_y: None
                        height: 20
                        halign: 'left'

                # ── Section label ──
                Label:
                    text: '学习工具'
                    font_name: 'ChineseFont'
                    font_size: '13sp'
                    bold: True
                    color: 0.302, 0.325, 0.349, 1
                    size_hint_y: None
                    height: 30
                    halign: 'left'
                    padding: [12, 0]

                # ── Card 1 : 学习 ──
                Button:
                    size_hint_y: None
                    height: 64
                    background_normal: ''
                    background_color: 1, 1, 1, 1
                    color: 0.067, 0.078, 0.086, 1
                    font_name: 'ChineseFont'
                    font_size: '17sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text: '📖  回译学习'
                    on_press: root.go_learn()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]

                # ── Card 2 : 复盘 ──
                Button:
                    size_hint_y: None
                    height: 64
                    background_normal: ''
                    background_color: 1, 1, 1, 1
                    color: 0.067, 0.078, 0.086, 1
                    font_name: 'ChineseFont'
                    font_size: '17sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text: '📊  复盘回顾'
                    on_press: root.go_review()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]

                # ── Card 3 : 收藏 ──
                Button:
                    size_hint_y: None
                    height: 64
                    background_normal: ''
                    background_color: 1, 1, 1, 1
                    color: 0.067, 0.078, 0.086, 1
                    font_name: 'ChineseFont'
                    font_size: '17sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text: '⭐  收藏夹'
                    on_press: root.go_favorites()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]

                # ── Card 4 : 表达库 ──
                Button:
                    size_hint_y: None
                    height: 64
                    background_normal: ''
                    background_color: 1, 1, 1, 1
                    color: 0.067, 0.078, 0.086, 1
                    font_name: 'ChineseFont'
                    font_size: '17sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text: '📝  表达库'
                    on_press: root.go_expressions()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]

                # ── Card 5 : 设置 ──
                Button:
                    size_hint_y: None
                    height: 56
                    background_normal: ''
                    background_color: 1, 1, 1, 1
                    color: 0.067, 0.078, 0.086, 1
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    halign: 'left'
                    valign: 'middle'
                    text: '⚙️  设置'
                    on_press: root.go_settings()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16, 16, 16, 16]

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