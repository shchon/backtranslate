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
from kivy.uix.screenmanager import ScreenManager
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


# ---- Uxcel Go 风格设计 Token ----
UXCEL_PRIMARY = (0.486, 0.361, 1.0, 1)        # #7C5CFF
UXCEL_PRIMARY_LIGHT = (0.6, 0.5, 1.0, 0.15)   # 半透明紫
UXCEL_ACCENT_PINK = (1.0, 0.42, 0.616, 1)     # #FF6B9D
UXCEL_BG = (1, 1, 1, 1)                       # #FFFFFF
UXCEL_CARD_BG = (1, 1, 1, 1)                  # #FFFFFF
UXCEL_CARD_BORDER = (0.91, 0.91, 0.93, 1)     # #E8E8ED
UXCEL_CARD_ACTIVE = (0.486, 0.361, 1.0, 1)    # #7C5CFF
UXCEL_TEXT_TITLE = (0, 0, 0, 1)               # #000000
UXCEL_TEXT_HEADING = (0.102, 0.102, 0.102, 1) # #1A1A1A
UXCEL_TEXT_SECONDARY = (0.557, 0.557, 0.576, 1) # #8E8E93
UXCEL_TEXT_MUTED = (0.4, 0.4, 0.4, 1)         # #666666
UXCEL_TAB_ACTIVE = (0.486, 0.361, 1.0, 1)     # #7C5CFF
UXCEL_TAB_INACTIVE = (0.78, 0.78, 0.80, 1)    # #C7C7CC
UXCEL_CORNER_CARD = 16
UXCEL_CORNER_BUTTON = 12


class BottomTabButton(Button):
    """Bottom navigation tab button with icon and label."""
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
        self.height = 60
        self._update_text()

    def set_active(self, active):
        self.is_active = active
        self._update_text()

    def _update_text(self):
        color = UXCEL_TAB_ACTIVE if self.is_active else UXCEL_TAB_INACTIVE
        r, g, b, a = color
        hex_color = f'{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        self.text = f'[color={hex_color}]{self.icon}[/color]\n[size=10][color={hex_color}]{self.label_text}[/color][/size]'


class BottomTabBar(BoxLayout):
    """Bottom tab bar with 5 tabs matching Uxcel style."""
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 72  # Tab bar height + bottom safe area
        self.padding = [0, 0, 0, 0]
        self.spacing = 0

        # Background
        with self.canvas.before:
            Color(rgba=(0.98, 0.98, 0.98, 1))  # Very light gray
            Rectangle(pos=self.pos, size=self.size)

        # Top border line
        with self.canvas.before:
            Color(rgba=(0.91, 0.91, 0.93, 1))  # #E8E8ED
            Line(width=0.5, points=[self.x, self.y + self.height - 72,
                                    self.x + self.width, self.y + self.height - 72])

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.tabs = []
        tab_items = [
            ("🏠", "首页", "home"),
            ("📖", "学习", "learn"),
            ("📊", "复盘", "review"),
            ("⭐", "收藏", "favorites"),
            ("⚙️", "设置", "settings"),
        ]

        for icon, label, screen_name in tab_items:
            tab = BottomTabButton(
                icon=icon,
                label=label,
                screen_name=screen_name,
            )
            tab.bind(on_press=self._on_tab_press)
            self.tabs.append(tab)
            self.add_widget(tab)

        # Set home as active by default
        self.set_active("home")

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0.98, 0.98, 0.98, 1))
            Rectangle(pos=self.pos, size=self.size)
            Color(rgba=(0.91, 0.91, 0.93, 1))
            Line(width=0.5, points=[self.x, self.y + self.height - 72,
                                    self.x + self.width, self.y + self.height - 72])

    def _on_tab_press(self, tab):
        self.sm.current = tab.screen_name
        self.set_active(tab.screen_name)

    def set_active(self, screen_name):
        for tab in self.tabs:
            tab.set_active(tab.screen_name == screen_name)


class MainLayout(BoxLayout):
    """Main app layout: ScreenManager + BottomTabBar."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 0
        self.padding = 0

        # Screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(LearnScreen(name="learn"))
        self.sm.add_widget(ReviewScreen(name="review"))
        self.sm.add_widget(FavoritesScreen(name="favorites"))
        self.sm.add_widget(ExpressionsScreen(name="expressions"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        # Tab bar
        self.tab_bar = BottomTabBar(screen_manager=self.sm)

        self.add_widget(self.sm)
        self.add_widget(self.tab_bar)

        # Track screen changes to update tab bar
        self.sm.bind(current=self._on_screen_change)

    def _on_screen_change(self, instance, screen_name):
        self.tab_bar.set_active(screen_name)


class BackTranslateApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "BackTranslate"
        self.session_id = None
        self.worker = None

    def build(self):
        # Initialize database
        init_db()

        # Set background color
        from kivy.core.window import Window
        Window.clearcolor = (1, 1, 1, 1)  # White background

        # Build main layout
        main_layout = MainLayout()

        # Start AI worker
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

        sm = self.root.sm
        review_screen = sm.get_screen("review")
        if review_screen and review_screen.session_id:
            try:
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

        sm = self.root.sm
        review_screen = sm.get_screen("review")
        if review_screen and review_screen.session_id:
            try:
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