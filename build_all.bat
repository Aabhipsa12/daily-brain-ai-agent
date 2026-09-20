@echo off
title Daily Brain - Master Build Orchestrator
color 0B
echo ============================================================
echo DAILY BRAIN - Unified Multi-Platform Build Pipeline
echo ============================================================
python "%~dp0build_all.py" %*
pause
