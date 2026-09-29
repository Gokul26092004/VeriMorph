@echo off
title VeriMorph Enterprise Web Dashboard
echo ===================================================================
echo   VeriMorph Enterprise AI Platform
echo   Starting web dashboard on http://localhost:8000 ...
echo ===================================================================
cd /d "%~dp0"
python run_app.py
pause
