@echo off
title Rent Valley monitor
cd /d "%~dp0"
echo Rent Valley monitor - provera svakih 10 minuta
echo Zaustavi: Ctrl+C
echo.
:loop
python monitor.py
echo.
echo [%date% %time%] Sledeca provera za 10 min...
timeout /t 600 /nobreak >nul
goto loop
