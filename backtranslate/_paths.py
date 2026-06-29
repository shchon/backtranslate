import os
import sys


def get_app_dir() -> str:
    """Return the directory where config/data should be stored.
    In dev: project root. In PyInstaller bundle: next to the .exe."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_config_dir() -> str:
    return os.path.join(get_app_dir(), "config")


def get_data_dir() -> str:
    return os.path.join(get_app_dir(), "data")
