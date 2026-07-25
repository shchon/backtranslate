#!/usr/bin/env python3
"""
BackTranslate Kivy App - Entry point for Android build.
This file is needed by python-for-android which looks for main.py
in the app directory. It simply imports and runs the real app.
"""
import os
import sys

# Ensure the project root is on sys.path
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from kivy_app.main import BackTranslateApp

if __name__ == '__main__':
    BackTranslateApp().run()