"""Settings screen — clean modern form."""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from backtranslate.config import load_config, save_config

Builder.load_string("""
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
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
            padding: [12, 0]
            canvas.before:
                Color:

                    rgba: 0.969, 0.973, 0.969, 1
                Rectangle:

                    pos: self.pos

                    size: self.size
            Button:
                text: '← 返回'
                size_hint_x: None
                width: 64
                background_normal: ''
                background_color: 0,0,0,0
                color: 0.420, 0.565, 0.502, 1
                font_name: 'ChineseFont'
                font_size: '16sp'
                on_press: root.go_home()
            Label:
                text: '设置'
                font_name: 'ChineseFont'
                font_size: '20sp'
                bold: True
                color: 0.067, 0.078, 0.086, 1
            Widget:
                size_hint_x: None
                width: 88

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: [20, 16]
                spacing: 14

                # ── API 地址 ──
                Label:
                    text: 'API 地址'
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    bold: True
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 22
                    halign: 'left'
                TextInput:
                    id: base_url_input
                    hint_text: '例如 https://api.deepseek.com'
                    hint_text_color: 0.420, 0.447, 0.475, 1
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    size_hint_y: None
                    height: 48
                    padding: [16, 12]
                    multiline: False
                    background_color: 1, 1, 1, 1
                    foreground_color: 0, 0, 0, 1

                # ── API Key ──
                Label:
                    text: 'API Key'
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    bold: True
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 22
                    halign: 'left'
                TextInput:
                    id: api_key_input
                    hint_text: '输入你的 API Key'
                    hint_text_color: 0.420, 0.447, 0.475, 1
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    size_hint_y: None
                    height: 48
                    padding: [16, 12]
                    multiline: False
                    password: True
                    background_color: 1, 1, 1, 1
                    foreground_color: 0, 0, 0, 1

                # ── 模型 ──
                Label:
                    text: '模型'
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    bold: True
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 22
                    halign: 'left'
                TextInput:
                    id: model_input
                    hint_text: '例如 deepseek-chat'
                    hint_text_color: 0.420, 0.447, 0.475, 1
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    size_hint_y: None
                    height: 48
                    padding: [16, 12]
                    multiline: False
                    background_color: 1, 1, 1, 1
                    foreground_color: 0, 0, 0, 1

                # ── 上下文 ──
                Label:
                    text: '上下文句数'
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    bold: True
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 22
                    halign: 'left'
                BoxLayout:
                    size_hint_y: None
                    height: 48
                    spacing: 12
                    TextInput:
                        id: context_input
                        text: '1'
                        font_name: 'ChineseFont'
                        font_size: '15sp'
                        size_hint_x: None
                        width: 80
                        padding: [16, 12]
                        multiline: False
                        input_filter: 'int'
                        background_color: 1, 1, 1, 1
                        foreground_color: 0, 0, 0, 1
                    Label:
                        text: '前后各取 N 句作为上下文'
                        font_name: 'ChineseFont'
                        font_size: '13sp'
                        color: 0.420, 0.447, 0.475, 1

                # ── 提示词 ──
                Label:
                    text: '提示词模板'
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    bold: True
                    color: 0.067, 0.078, 0.086, 1
                    size_hint_y: None
                    height: 22
                    halign: 'left'
                TextInput:
                    id: prompt_input
                    hint_text: 'AI 评分提示词模板……'
                    hint_text_color: 0.420, 0.447, 0.475, 1
                    font_name: 'ChineseFont'
                    font_size: '14sp'
                    size_hint_y: None
                    height: 140
                    padding: [16, 14]
                    background_color: 1, 1, 1, 1
                    foreground_color: 0, 0, 0, 1

                # ── Save ──
                Button:
                    text: '保存设置'
                    font_name: 'ChineseFont'
                    font_size: '16sp'
                    bold: True
                    size_hint_y: None
                    height: 48
                    color: 1, 1, 1, 1
                    background_normal: ''
                    background_color: 0.420, 0.565, 0.502, 1
                    on_press: root.save_settings()

                # ── Reset ──
                Button:
                    text: '恢复默认'
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    size_hint_y: None
                    height: 48
                    color: 0.302, 0.325, 0.349, 1
                    background_normal: ''
                    background_color: 0.890, 0.898, 0.886, 1
                    on_press: root.reset_defaults()

                Widget:
                    size_hint_y: None
                    height: 40
""")


class SettingsScreen(Screen):
    def on_enter(self):
        cfg = load_config()
        self.ids.base_url_input.text = cfg.get("base_url", "")
        self.ids.api_key_input.text = cfg.get("api_key", "")
        self.ids.model_input.text = cfg.get("model", "deepseek-chat")
        self.ids.context_input.text = str(cfg.get("context_n", 1))
        self.ids.prompt_input.text = cfg.get("prompt_template", "")

    def save_settings(self):
        cfg = load_config()
        cfg["base_url"] = self.ids.base_url_input.text.strip()
        cfg["api_key"] = self.ids.api_key_input.text.strip()
        cfg["model"] = self.ids.model_input.text.strip()
        try:
            cfg["context_n"] = int(self.ids.context_input.text.strip() or "1")
        except ValueError:
            cfg["context_n"] = 1
        cfg["prompt_template"] = self.ids.prompt_input.text
        save_config(cfg)
        self._toast("已保存")

    def reset_defaults(self):
        self.ids.base_url_input.text = ""
        self.ids.api_key_input.text = ""
        self.ids.model_input.text = "deepseek-chat"
        self.ids.context_input.text = "1"
        self.ids.prompt_input.text = ""
        save_config({"base_url": "", "api_key": "", "model": "deepseek-chat",
                      "context_n": 1, "prompt_template": ""})
        self._toast("已恢复默认值")

    def _toast(self, msg):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.clock import Clock
        popup = Popup(title='', content=Label(text=msg, font_name='ChineseFont',
            font_size='15sp', color=(0.102,0.110,0.118,1)),
            size_hint=(0.5,0.15), auto_dismiss=True)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def go_home(self):
        self.manager.current = "home"
