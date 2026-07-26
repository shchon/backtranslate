"""
BackTranslate - 回译训练 (Kivy Android App)
Entry point for the Kivy-based mobile version.
"""
import os
import sys
import json

# Ensure the project root is on sys.path so we can import backtranslate.*
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ---- 字体配置 (必须在 Kivy 初始化之前) ----
_font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
_font_path = os.path.join(_font_dir, 'msyh.ttc')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'NotoSansSC-Regular.otf')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'NotoSansSC.otf')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'wqy-microhei.ttc')
if os.path.exists(_font_path):
    try:
        from kivy.config import Config
        Config.set('kivy', 'default_font', [
            'ChineseFont',
            _font_path,
        ])
    except Exception as e:
        print(f'Font config warning: {e}')
    else:
        print(f'Using font: {_font_path}')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line

# Register Chinese font - override Roboto (Kivy default) with our font
if os.path.exists(_font_path):
    try:
        LabelBase.register(name='Roboto', fn_regular=_font_path)
        LabelBase.register(name='ChineseFont', fn_regular=_font_path)
    except Exception as e:
        print(f'Font registration warning: {e}')

from backtranslate.database.connection import init_db
from backtranslate.config import load_config, save_config
from backtranslate.database.operations import (
    update_evaluation_status, get_subtitles_for_session,
    create_session, create_subtitles_batch,
)

from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.learn_screen import LearnScreen
from kivy_app.screens.review_screen import ReviewScreen
from kivy_app.screens.favorites_screen import FavoritesScreen
from kivy_app.screens.expressions_screen import ExpressionsScreen
from kivy_app.screens.settings_screen import SettingsScreen
from kivy_app.worker import EvaluationWorker


# ============================================================
#  KakaoBank iOS 风格设计 Token
# ============================================================
# 背景
KBANK_BG = (0.965, 0.965, 0.965, 1)          # #F6F6F6  全局背景
KBANK_BG_WHITE = (1, 1, 1, 1)                 # #FFFFFF  白色卡片/面板

# 功能卡片颜色（4色系统）
KBANK_CARD_MINT = (0.776, 0.894, 0.827, 1)    # #C6E4D3  薄荷绿 → 学习
KBANK_CARD_ORANGE = (0.953, 0.490, 0.369, 1)  # #F37D5E  珊瑚橙 → 复习
KBANK_CARD_BLUE = (0.318, 0.529, 0.651, 1)    # #5187A6  钢蓝 → 表达库
KBANK_CARD_KHAKI = (0.788, 0.761, 0.682, 1)   # #C9C2AE  卡其 → 收藏

# 卡片内按钮（同色系浅色）
KBANK_BTN_MINT = (0.839, 0.906, 0.867, 1)     # #D6E7DD
KBANK_BTN_ORANGE = (0.973, 0.686, 0.561, 1)   # #F8AF8F
KBANK_BTN_BLUE = (0.569, 0.694, 0.769, 1)     # #91B1C4
KBANK_BTN_KHAKI = (0.871, 0.851, 0.780, 1)    # #DED9C7

# 文字颜色
KBANK_TEXT_TITLE = (0.067, 0.067, 0.067, 1)      # #111111  主标题
KBANK_TEXT_BODY = (0.165, 0.165, 0.165, 1)        # #2A2A2A  正文
KBANK_TEXT_SECONDARY = (0.533, 0.533, 0.533, 1)   # #888888  辅助说明
KBANK_TEXT_WHITE = (1, 1, 1, 1)                   # #FFFFFF  深色卡片上的文字
KBANK_TEXT_MUTED_WHITE = (0.973, 0.906, 0.875, 1) # #F8E7DF  深色卡片上的辅助文字

# Tab 栏
KBANK_TAB_ACTIVE = (0.067, 0.067, 0.067, 1)     # #111111  选中
KBANK_TAB_INACTIVE = (0.6, 0.6, 0.6, 1)          # #999999  未选中
KBANK_TAB_BG = (1, 1, 1, 1)                       # #FFFFFF  Tab 背景
KBANK_TAB_SEPARATOR = (0.886, 0.914, 0.898, 1)    # #E2E9E5  Tab 顶部分隔线

# 圆角 & 尺寸
KBANK_CARD_RADIUS = 28       # 卡片圆角
KBANK_BUTTON_RADIUS = 20     # 按钮圆角
KBANK_BUTTON_HEIGHT = 48     # 按钮高度
KBANK_TAB_BAR_HEIGHT = 84    # 底部 Tab 栏总高度
KBANK_NAV_BAR_HEIGHT = 56    # 顶部导航栏高度
KBANK_GLOBAL_MARGIN = 16     # 全局左右边距
KBANK_CARD_PADDING = 24      # 卡片内边距
KBANK_CARD_GAP = 16          # 卡片间距
KBANK_SEPARATOR_HEIGHT = 1   # 分隔线高度

# 阴影 (Kivy 无法原生实现完整阴影，用描边+轻微 inset 模拟)
KBANK_SHADOW_COLOR = (0, 0, 0, 0.08)


# ============================================================
#  BottomTabButton
# ============================================================
class BottomTabButton(Button):
    """底部导航标签按钮 — KakaoBank 风格."""
    def __init__(self, icon="", label="", screen_name="", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.label_text = label
        self.screen_name = screen_name
        self.is_active = False
        self.markup = True
        self.font_name = 'ChineseFont'
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.size_hint_y = None
        self.height = 84
        self._update_text()

    def set_active(self, active):
        self.is_active = active
        self._update_text()

    def _update_text(self):
        r, g, b, _a = KBANK_TAB_ACTIVE if self.is_active else KBANK_TAB_INACTIVE
        hex_color = f'{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        weight = 'bold' if self.is_active else ''
        self.text = (
            f'[color={hex_color}][size=20]{self.icon}[/size][/color]\n'
            f'[size=11][color={hex_color}]{self.label_text}[/color][/size]'
        )


# ============================================================
#  BottomTabBar
# ============================================================
class BottomTabBar(BoxLayout):
    """底部 Tab 栏 — KakaoBank 风格：白色背景，顶部 1pt 分隔线."""
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 84
        self.padding = [0, 0, 0, 0]
        self.spacing = 0

        self.bind(pos=self._redraw, size=self._redraw)

        self.tabs = []
        tab_items = [
            ("🏠", "首页", "home"),
            ("📖", "学习", "learn"),
            ("📊", "复盘", "review"),
            ("⭐", "收藏", "favorites"),
            ("⚙️", "设置", "settings"),
        ]

        for icon, label, screen_name in tab_items:
            tab = BottomTabButton(icon=icon, label=label, screen_name=screen_name)
            tab.bind(on_press=self._on_tab_press)
            self.tabs.append(tab)
            self.add_widget(tab)

        self.set_active("home")

    def _redraw(self, *args):
        self.canvas.before.clear()
        # 白色背景
        with self.canvas.before:
            Color(rgba=KBANK_TAB_BG)
            Rectangle(pos=self.pos, size=self.size)
            # 顶部 1pt 分隔线
            Color(rgba=KBANK_TAB_SEPARATOR)
            Line(width=1, points=[
                self.x, self.y + self.height,
                self.x + self.width, self.y + self.height,
            ])

    def _on_tab_press(self, tab):
        self.sm.current = tab.screen_name
        self.set_active(tab.screen_name)

    def set_active(self, screen_name):
        for tab in self.tabs:
            tab.set_active(tab.screen_name == screen_name)


# ============================================================
#  MainLayout
# ============================================================
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 0
        self.padding = 0

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(LearnScreen(name="learn"))
        self.sm.add_widget(ReviewScreen(name="review"))
        self.sm.add_widget(FavoritesScreen(name="favorites"))
        self.sm.add_widget(ExpressionsScreen(name="expressions"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        self.tab_bar = BottomTabBar(screen_manager=self.sm)

        self.add_widget(self.sm)
        self.add_widget(self.tab_bar)

        self.sm.bind(current=self._on_screen_change)

    def _on_screen_change(self, instance, screen_name):
        self.tab_bar.set_active(screen_name)


# ============================================================
#  App
# ============================================================
class BackTranslateApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "BackTranslate"
        self.session_id = None
        self.worker = None

    def build(self):
        init_db()

        from kivy.core.window import Window
        Window.clearcolor = KBANK_BG  # #F6F6F6

        main_layout = MainLayout()
        self._start_worker()
        Window.bind(on_keyboard=self._on_key_back)
        return main_layout

    def _start_worker(self):
        cfg = load_config()
        self.worker = EvaluationWorker(
            base_url=cfg.get("base_url", ""),
            api_key=cfg.get("api_key", ""),
            model=cfg.get("model", ""),
            prompt_template=cfg.get("prompt_template", ""),
        )
        self.worker.on_done = self._on_eval_done
        self.worker.on_failed = self._on_eval_failed
        self.worker.start()

    def _on_eval_done(self, eval_id, result):
        try:
            update_evaluation_status(
                eval_id, "done",
                result["meaning_score"],
                result["grammar_score"],
                result["naturalness_score"],
                result["subtitle_style_score"],
                result["analysis"],
                json.dumps(result.get("suggested_expressions", [])),
            )
        except Exception:
            return

        try:
            sm = self.root.sm
            review_screen = sm.get_screen("review")
            if review_screen and review_screen.session_id:
                from backtranslate.database.connection import get_connection
                conn = get_connection()
                row = conn.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id = t.id "
                    "WHERE e.id = ?", (eval_id,)
                ).fetchone()
                conn.close()
                if row:
                    review_screen.update_evaluation(row[0])
        except Exception:
            pass

    def _on_eval_failed(self, eval_id):
        try:
            update_evaluation_status(eval_id, "failed", error="批改失败")
        except Exception:
            return

        try:
            sm = self.root.sm
            review_screen = sm.get_screen("review")
            if review_screen and review_screen.session_id:
                from backtranslate.database.connection import get_connection
                conn = get_connection()
                row = conn.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id = t.id "
                    "WHERE e.id = ?", (eval_id,)
                ).fetchone()
                conn.close()
                if row:
                    review_screen.update_evaluation(row[0])
        except Exception:
            pass

    def _on_key_back(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            sm = self.root.sm
            if sm.current != "home":
                sm.current = "home"
                return True
        return False

    def on_stop(self):
        if self.worker:
            self.worker.stop()


if __name__ == "__main__":
    if platform == 'android' and os.path.exists(_font_path):
        from kivy.core.text import LabelBase
        try:
            LabelBase.register(name='Roboto', fn_regular=_font_path)
        except Exception:
            pass
    BackTranslateApp().run()
