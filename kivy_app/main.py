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

# 功能卡片颜色（4色系统）
KBANK_CARD_MINT = (0.776, 0.894, 0.827, 1)    # #C6E4D3  薄荷绿 → 学习
KBANK_CARD_ORANGE = (0.953, 0.490, 0.369, 1)  # #F37D5E  珊瑚橙 → 复习
KBANK_CARD_BLUE = (0.318, 0.529, 0.651, 1)    # #5187A6  钢蓝 → 表达库
KBANK_CARD_KHAKI = (0.788, 0.761, 0.682, 1)   # #C9C2AE  卡其 → 收藏
KBANK_CARD_KHAKI_LIGHT = (0.871, 0.851, 0.780, 1)  # #DED9C7  卡其浅色按钮

# 文字颜色
KBANK_TEXT_TITLE = (0.067, 0.067, 0.067, 1)      # #111111  主标题
KBANK_TEXT_BODY = (0.165, 0.165, 0.165, 1)        # #2A2A2A  正文
KBANK_TEXT_SECONDARY = (0.533, 0.533, 0.533, 1)   # #888888  辅助说明

# 圆角 & 尺寸
KBANK_CARD_RADIUS = 28       # 卡片圆角
KBANK_NAV_BAR_HEIGHT = 56    # 顶部导航栏高度
KBANK_GLOBAL_MARGIN = 16     # 全局左右边距


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

        self.add_widget(self.sm)


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
