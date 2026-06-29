import json
import os
from .defaults import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_CONTEXT_N,
    DEFAULT_FONT_SIZE,
    DEFAULT_PROMPT_TEMPLATE,
)

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")


def _ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def _default_config():
    return {
        "base_url": DEFAULT_BASE_URL,
        "api_key": "",
        "model": DEFAULT_MODEL,
        "context_n": DEFAULT_CONTEXT_N,
        "font_size": DEFAULT_FONT_SIZE,
        "prompt_template": DEFAULT_PROMPT_TEMPLATE,
    }


def load_config() -> dict:
    _ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
        except (json.JSONDecodeError, ValueError):
            saved = {}
        cfg = _default_config()
        cfg.update(saved)
        return cfg
    return _default_config()


def save_config(cfg: dict) -> None:
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
