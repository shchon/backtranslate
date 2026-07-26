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

                # ── Test connection ──
                Button:
                    text: '🔄 测试连接'
                    font_name: 'ChineseFont'
                    font_size: '15sp'
                    size_hint_y: None
                    height: 48
                    color: 0.420, 0.565, 0.502, 1
                    background_normal: ''
                    background_color: 0.910, 0.941, 0.925, 1
                    on_press: root.test_connection()

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
        from kivy.uix.boxlayout import BoxLayout
        from kivy.graphics import Color, RoundedRectangle
        from kivy.clock import Clock

        content = BoxLayout(padding=[20, 14])
        with content.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[16, 16, 16, 16])
        content.add_widget(Label(text=msg, font_name='ChineseFont',
            font_size='15sp', color=(0.067, 0.078, 0.086, 1)))

        popup = Popup(title='', content=content,
            size_hint=(0.7, None), height=60, auto_dismiss=True)
        popup.title_color = (0.067, 0.078, 0.086, 1)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

        def _refresh_bg(inst, _):
            inst.canvas.before.clear()
            with inst.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                RoundedRectangle(pos=inst.pos, size=inst.size, radius=[16, 16, 16, 16])
        content.bind(pos=_refresh_bg, size=_refresh_bg)

    def test_connection(self):
        """Test the AI API connection with current settings."""
        import requests
        from kivy.clock import Clock

        base_url = self.ids.base_url_input.text.strip()
        api_key = self.ids.api_key_input.text.strip()
        model = self.ids.model_input.text.strip()

        if not base_url:
            self._toast("请先输入 API 地址")
            return
        if not api_key:
            self._toast("请先输入 API Key")
            return
        if not model:
            self._toast("请先输入模型名称")
            return

        self.save_settings()

        def _do():
            url = base_url.rstrip("/")
            if not url.endswith("/chat/completions"):
                url += "/chat/completions"

            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "返回 OK 即可"}],
                "max_tokens": 10,
                "temperature": 0.1,
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    Clock.schedule_once(lambda dt: self._toast(
                        f"✅ 连接成功！模型响应: {content[:50]}"))
                elif resp.status_code == 401:
                    Clock.schedule_once(lambda dt: self._toast("❌ 认证失败，请检查 API Key"))
                elif resp.status_code == 404:
                    Clock.schedule_once(lambda dt: self._toast("❌ API 地址或模型不存在 (404)"))
                else:
                    Clock.schedule_once(lambda dt: self._toast(
                        f"❌ 错误 {resp.status_code}: {resp.text[:60]}"))
            except requests.exceptions.ConnectTimeout:
                Clock.schedule_once(lambda dt: self._toast("❌ 连接超时，请检查 API 地址"))
            except requests.exceptions.ConnectionError:
                Clock.schedule_once(lambda dt: self._toast("❌ 无法连接，请检查网络和 API 地址"))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._toast(f"❌ {str(e)[:50]}"))

        import threading
        self._toast("⏳ 正在测试连接……")
        threading.Thread(target=_do, daemon=True).start()

    def go_home(self):
        self.manager.current = "home"
