from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame,
)
from PySide6.QtCore import Qt


NAV_STYLE = """
QPushButton {
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    color: #333;
}
QPushButton:hover {
    background: #e8e8e8;
}
QPushButton[active="true"] {
    background: #d0e0ff;
    font-weight: bold;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BackTranslate - 回译训练")
        self.resize(1100, 750)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("background: #f5f5f5;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 12, 8, 12)
        sidebar_layout.setSpacing(4)

        self.nav_buttons = []
        nav_items = ["学习", "复盘", "表达库", "设置"]

        for name in nav_items:
            btn = QPushButton(name)
            btn.setStyleSheet(NAV_STYLE)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, n=name: self._on_nav(n))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append((name, btn))

        sidebar_layout.addStretch()
        layout.addWidget(sidebar)

        # Content area
        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 1)

        self.learn_page = None
        self.review_page = None
        self.expressions_page = None
        self.settings_page = None

        self._update_nav("学习")

    def _on_nav(self, name: str) -> None:
        self._update_nav(name)
        if name == "学习" and self.learn_page:
            self.stack.setCurrentWidget(self.learn_page)
        elif name == "复盘" and self.review_page:
            self.stack.setCurrentWidget(self.review_page)
        elif name == "表达库" and self.expressions_page:
            self.stack.setCurrentWidget(self.expressions_page)
        elif name == "设置" and self.settings_page:
            self.stack.setCurrentWidget(self.settings_page)

    def _update_nav(self, active_name: str) -> None:
        for name, btn in self.nav_buttons:
            btn.setProperty("active", name == active_name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def set_learn_page(self, widget: QWidget) -> None:
        self.learn_page = widget
        self.stack.addWidget(widget)

    def set_review_page(self, widget: QWidget) -> None:
        self.review_page = widget
        self.stack.addWidget(widget)

    def set_expressions_page(self, widget: QWidget) -> None:
        self.expressions_page = widget
        self.stack.addWidget(widget)

    def set_settings_page(self, widget: QWidget) -> None:
        self.settings_page = widget
        self.stack.addWidget(widget)

    def navigate_to_review(self) -> None:
        self._on_nav("复盘")
