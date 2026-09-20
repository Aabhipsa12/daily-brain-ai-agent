@echo off
title Daily Brain Shortcut Installer
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_desktop_shortcut.ps1"
echo.
echo ========================================================
echo   Daily Brain shortcut has been placed on your Desktop!
echo ========================================================
echo.
pause