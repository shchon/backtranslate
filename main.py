#!/usr/bin/env python3
"""
BackTranslate Kivy App - Entry point for Android build.
"""
import os
import sys
import traceback

# Log crash info to a file
_crash_log = '/data/data/org.backtranslate.backtranslate/files/app/crash.log'
try:
    _crash_log = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'crash.log'
    )
except Exception:
    _crash_log = '/sdcard/backtranslate_crash.log'

def _log_error(msg):
    try:
        with open(_crash_log, 'w', encoding='utf-8') as f:
            f.write(msg)
    except Exception:
        pass

try:
    # Ensure the project root is on sys.path
    _project_root = os.path.dirname(os.path.abspath(__file__))
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

    from kivy_app.main import BackTranslateApp

    if __name__ == '__main__':
        BackTranslateApp().run()

except Exception as e:
    error_msg = f"CRASH: {e}\n\n{traceback.format_exc()}"
    _log_error(error_msg)
    print(error_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    raise