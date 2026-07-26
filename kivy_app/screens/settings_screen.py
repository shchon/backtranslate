"""
Settings screen - API configuration and app settings.
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.clock import Clock

from backtranslate.config import load_config, save_config
from backtranslate.defaults import (
    DEFAULT_BASE_URL, DEFAULT_MODEL, DEFAULT_CONTEXT_N,
    DEFAULT_PROMPT_TEMPLATE,
)

Builder.load_string("""
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 0

        # Top bar - Uxcel style
        BoxLayout:
            size_hint_y: None
            height: 60
            padding: [12, 0]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '‹ 返回'
                size_hint_x: None
                width: 60
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.486, 0.361, 1.0, 1
                font_size: '17sp'
                on_press: root.go_home()
            Label:
                text: '设置'
                font_size: '18sp'
                bold: True
                color: 0.102, 0.102, 0.102, 1
            Widget:
                size_hint_x: None
                width: 60

        # Scrollable settings form
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [20, 16]
                spacing: 16

                # API Base URL
                Label:
                    text: 'API 地址'
                    font_size: '15sp'
                    bold: True
                    color: 0.102, 0.102, 0.102, 1
                    size_hint_y: None
                    height: 24
                    halign: 'left'
                TextInput:
                    id: base_url_input
                    hint_text: '例如: https://api.deepseek.com'
                    font_size: '16sp'
                    size_hint_y: None
                    height: 52
                    padding: [16, 14]
                    multiline: False
                    canvas.before:
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

                # API Key
                Label:
                    text: 'API Key'
                    font_size: '15sp'
                    bold: True
                    color: 0.102, 0.102, 0.102, 1
                    size_hint_y: None
                    height: 24
                    halign: 'left'
                TextInput:
                    id: api_key_input
                    hint_text: '输入你的 API Key'
                    font_size: '16sp'
                    size_hint_y: None
                    height: 52
                    padding: [16, 14]
                    multiline: False
                    password: True
                    canvas.before:
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

                # Model
                Label:
                    text: '模型'
                    font_size: '15sp'
                    bold: True
                    color: 0.102, 0.102, 0.102, 1
                    size_hint_y: None
                    height: 24
                    halign: 'left'
                TextInput:
                    id: model_input
                    hint_text: '例如: deepseek-chat'
                    font_size: '16sp'
                    size_hint_y: None
                    height: 52
                    padding: [16, 14]
                    multiline: False
                    canvas.before:
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

                # Context sentences
                Label:
                    text: '上下文句数'
                    font_size: '15sp'
                    bold: True
                    color: 0.102, 0.102, 0.102, 1
                    size_hint_y: None
                    height: 24
                    halign: 'left'
                BoxLayout:
                    size_hint_y: None
                    height: 52
                    spacing: 12
                    TextInput:
                        id: context_input
                        text: '1'
                        font_size: '16sp'
                        size_hint_x: None
                        width: 80
                        padding: [16, 14]
                        multiline: False
                        input_filter: 'int'
                        canvas.before:
                            Color:
                                rgba: 0.91, 0.91, 0.93, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [12, 12, 12, 12]
                    Label:
                        text: '句（前后各取N句作为上下文）'
                        font_size: '14sp'
                        color: 0.557, 0.557, 0.576, 1

                # Prompt template
                Label:
                    text: '提示词模板'
                    font_size: '15sp'
                    bold: True
                    color: 0.102, 0.102, 0.102, 1
                    size_hint_y: None
                    height: 24
                    halign: 'left'
                TextInput:
                    id: prompt_input
                    hint_text: 'AI 评分提示词模板...'
                    font_size: '14sp'
                    size_hint_y: None
                    height: 200
                    padding: [16, 14]
                    canvas.before:
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

                # Save button - Uxcel style
                Button:
                    text: '💾 保存设置'
                    size_hint_y: None
                    height: 52
                    background_normal: ''
                    background_color: 0.486, 0.361, 1.0, 1
                    color: 1, 1, 1, 1
                    font_size: '16sp'
                    bold: True
                    on_press: root.save_settings()
                    canvas.before:
                        Color:
                            rgba: 0.486, 0.361, 1.0, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]

                # Reset button
                Button:
                    text: '↺ 恢复默认'
                    size_hint_y: None
                    height: 48
                    background_normal: ''
                    background_color: 0.95, 0.95, 0.97, 1
                    color: 0.4, 0.4, 0.4, 1
                    font_size: '15sp'
                    on_press: root.reset_defaults()
                    canvas.before:
                        Color:
                            rgba: 0.95, 0.95, 0.97, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12, 12, 12, 12]
                        Color:
                            rgba: 0.91, 0.91, 0.93, 1
                        Line:
                            rounded_rectangle: self.pos[0], self.pos[1], self.size[0], self.size[1], 12
                            width: 0.5

                # Bottom spacing
                Widget:
                    size_hint_y: None
                    height: 40
""")


class SettingsScreen(Screen):
    def on_enter(self):
        """Load current settings into the form."""
        cfg = load_config()
        self.ids.base_url_input.text = cfg.get("base_url", DEFAULT_BASE_URL)
        self.ids.api_key_input.text = cfg.get("api_key", "")
        self.ids.model_input.text = cfg.get("model", DEFAULT_MODEL)
        self.ids.context_input.text = str(cfg.get("context_n", DEFAULT_CONTEXT_N))
        self.ids.prompt_input.text = cfg.get("prompt_template", DEFAULT_PROMPT_TEMPLATE)

    def save_settings(self):
        """Save settings and restart the AI worker."""
        try:
            context_n = int(self.ids.context_input.text.strip())
        except ValueError:
            context_n = DEFAULT_CONTEXT_N

        cfg = {
            "base_url": self.ids.base_url_input.text.strip(),
            "api_key": self.ids.api_key_input.text.strip(),
            "model": self.ids.model_input.text.strip(),
            "context_n": context_n,
            "prompt_template": self.ids.prompt_input.text.strip(),
        }
        save_config(cfg)

        # Restart AI worker with new settings
        app = self._get_app()
        if app and app.worker:
            app.worker.stop()
            app._start_worker()

        self._show_toast("设置已保存")

    def reset_defaults(self):
        """Reset to default settings."""
        self.ids.base_url_input.text = DEFAULT_BASE_URL
        self.ids.api_key_input.text = ""
        self.ids.model_input.text = DEFAULT_MODEL
        self.ids.context_input.text = str(DEFAULT_CONTEXT_N)
        self.ids.prompt_input.text = DEFAULT_PROMPT_TEMPLATE

    def _show_toast(self, message):
        """Show a brief popup notification."""
        popup = Popup(
            title='',
            content=Label(
                text=message,
                font_size='16sp',
                color=(0.2, 0.2, 0.2, 1),
            ),
            size_hint=(0.6, 0.25),
            auto_dismiss=False,
        )
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
        popup.open()

    def _get_app(self):
        from kivy.app import App
        return App.get_running_app()

    def go_home(self):
        self.manager.current = "home"