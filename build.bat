@echo off
echo ========================================
echo   Quick Translator - Build Script
echo ========================================
echo.

echo [1/3] Installing dependencies...
pip install pyinstaller

echo.
echo [2/3] Building executable...
pyinstaller --clean quicktranslator.spec

echo.
echo [3/3] Build complete!
echo.
echo Output: dist\QuickTranslator.exe
echo.
echo To create installer:
echo   1. Install Inno Setup from https://jrsoftware.org/isinfo.php
echo   2. Right-click installer.iss and select "Compile"
echo   3. Installer will be in installer_output folder
echo.
pause
