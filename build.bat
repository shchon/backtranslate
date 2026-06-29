@echo off
echo ========================================
echo  BackTranslate 打包工具
echo ========================================

REM 确认 PyInstaller 已安装
pip install pyinstaller 2>nul

REM 清理旧构建
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo 正在打包...

pyinstaller --noconfirm ^
    --name "BackTranslate" ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-data "backtranslate;backtranslate" ^
    --hidden-import "PySide6.QtCore" ^
    --hidden-import "PySide6.QtWidgets" ^
    --hidden-import "PySide6.QtGui" ^
    --collect-all "PySide6" ^
    backtranslate\main.py

echo.
echo ========================================
echo  打包完成！文件在 dist\BackTranslate.exe
echo ========================================
echo.
echo 拷贝到其他电脑直接运行即可。
echo 首次运行时会在同目录自动创建 config 和 data 文件夹。
pause
