"""
BackTranslate    回译训练
Kivy Android App — Clean Modern UI
"""
import os, sys, json

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ── 字体 ──
_font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
_font_path = os.path.join(_font_dir, 'msyh.ttc')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'NotoSansSC-Regular.otf')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'NotoSansSC.otf')
if not os.path.exists(_font_path):
    _font_path = os.path.join(_font_dir, 'wqy-microhei.ttc')

if os.path.exists(_font_path):
    from kivy.config import Config
    Config.set('kivy', 'default_font', ['ChineseFont', _font_path])

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import platform

if os.path.exists(_font_path):
    LabelBase.register(name='Roboto', fn_regular=_font_path)
    LabelBase.register(name='ChineseFont', fn_regular=_font_path)

from backtranslate.database.connection import init_db
from backtranslate.config import load_config
from backtranslate.database.operations import update_evaluation_status

from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.learn_screen import LearnScreen
from kivy_app.screens.review_screen import ReviewScreen
from kivy_app.screens.favorites_screen import FavoritesScreen
from kivy_app.screens.expressions_screen import ExpressionsScreen
from kivy_app.screens.settings_screen import SettingsScreen
from kivy_app.worker import EvaluationWorker


# ═══════════════════════════════════════════════════════════
#  DESIGN SYSTEM  —  清爽现代 / Material Design 3 风格
# ═══════════════════════════════════════════════════════════

# ── 主色系 (Sage Green 鼠尾草绿) ──
PRIMARY      = (0.420, 0.565, 0.502, 1)    # #6B9080  主色
PRIMARY_LIGHT = (0.910, 0.941, 0.925, 1)   # #E8F0EC  主色浅底
PRIMARY_DARK  = (0.306, 0.455, 0.392, 1)   # #4E7464  主色深

# ── 功能色 ──
ACCENT_BLUE   = (0.376, 0.533, 0.820, 1)   # #6088D1  蓝色强调
ACCENT_AMBER  = (0.925, 0.596, 0.235, 1)   # #EC983C  琥珀色
ACCENT_CORAL  = (0.878, 0.345, 0.298, 1)   # #E0584C  警示红
ACCENT_GREEN  = (0.357, 0.620, 0.490, 1)   # #5B9E7D  成功绿

# ── 背景 ──
BG_PAGE   = (0.969, 0.973, 0.969, 1)       # #F7F8F7  页面底
BG_CARD   = (1, 1, 1, 1)                   # #FFFFFF  卡片
BG_SURFACE = (0.953, 0.957, 0.953, 1)      # #F3F4F3  次级表面

# ── 文字 ──
TEXT_PRIMARY   = (0.102, 0.110, 0.118, 1)   # #1A1C1E  主文字
TEXT_SECONDARY = (0.408, 0.439, 0.471, 1)   # #687078  辅助文字
TEXT_MUTED     = (0.616, 0.643, 0.667, 1)   # #9DA4AA  弱化文字
TEXT_ON_DARK   = (1, 1, 1, 1)              # #FFFFFF  深底白字
TEXT_ON_DARK_MUTED = (0.8, 0.84, 0.82, 1)  # 深底弱化

# ── 边界 / 分割 ──
BORDER_LIGHT = (0.902, 0.910, 0.902, 1)    # #E6E8E6  浅边框
SEPARATOR    = (0.937, 0.941, 0.937, 1)    # #EFF0EF  分割线

# ── 圆角 ──
RADIUS_CARD   = 16   # 卡片
RADIUS_BTN    = 12   # 按钮
RADIUS_INPUT  = 12   # 输入框
RADIUS_CHIP   = 20   # 标签/ chip

# ── 尺寸 (dp) ──
NAV_BAR_H    = 56   # 顶栏
BTN_H        = 48   # 按钮高
INPUT_H      = 52   # 输入框高
CARD_PAD     = 16   # 卡片内边距
PAGE_MARGIN  = 16   # 页面边距
ITEM_GAP     = 12   # 列表项间距
SECTION_GAP  = 16   # 区块间距

# ── 字体层级 ──
FONT_DISPLAY  = '28sp'  # 首页问候
FONT_HEADLINE = '22sp'  # 页面标题
FONT_TITLE    = '18sp'  # 卡片标题
FONT_BODY     = '16sp'  # 正文
FONT_LABEL    = '14sp'  # 标签
FONT_CAPTION  = '12sp'  # 小字
FONT_BTN      = '16sp'  # 按钮

# ── 阴影 (Kivy 不支持原生阴影，用轻微偏移模拟) ──
SHADOW_DOWN  = (0, 0.02, 0.04, 0.06)   # 向下阴影色
SHADOW_UP    = (0, -0.01, 0.02, 0.04)  # 向上阴影


# ═══════════════════════════════════════════════════════════
#  MainLayout
# ═══════════════════════════════════════════════════════════
class MainLayout(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
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


# ═══════════════════════════════════════════════════════════
#  App
# ═══════════════════════════════════════════════════════════
class BackTranslateApp(App):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title = "BackTranslate"
        self.worker = None

    def build(self):
        init_db()
        Window.clearcolor = BG_PAGE
        layout = MainLayout()
        self._start_worker()
        Window.bind(on_keyboard=self._on_key_back)
        return layout

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
            update_evaluation_status(eval_id, "done",
                result["meaning_score"], result["grammar_score"],
                result["naturalness_score"], result["subtitle_style_score"],
                result["analysis"],
                json.dumps(result.get("suggested_expressions", [])))
        except Exception:
            return
        try:
            sm = self.root.sm
            rs = sm.get_screen("review")
            if rs and rs.session_id:
                from backtranslate.database.connection import get_connection
                c = get_connection()
                row = c.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id=t.id "
                    "WHERE e.id=?", (eval_id,)).fetchone()
                c.close()
                if row:
                    rs.update_evaluation(row[0])
        except Exception:
            pass

    def _on_eval_failed(self, eval_id):
        try:
            update_evaluation_status(eval_id, "failed", error="批改失败")
        except Exception:
            return
        try:
            sm = self.root.sm
            rs = sm.get_screen("review")
            if rs and rs.session_id:
                from backtranslate.database.connection import get_connection
                c = get_connection()
                row = c.execute(
                    "SELECT t.subtitle_id FROM translations t "
                    "JOIN evaluations e ON e.translation_id=t.id "
                    "WHERE e.id=?", (eval_id,)).fetchone()
                c.close()
                if row:
                    rs.update_evaluation(row[0])
        except Exception:
            pass

    def _on_key_back(self, window, key, *args):
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
        LabelBase.register(name='Roboto', fn_regular=_font_path)
    BackTranslateApp().run()
