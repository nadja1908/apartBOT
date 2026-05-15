@echo off
cd /d "%~dp0"
python monitor.py
if errorlevel 1 pause
