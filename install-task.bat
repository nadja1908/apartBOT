@echo off
cd /d "%~dp0"
set TASK_NAME=RentValleyMonitor
set SCRIPT=%~dp0run.bat

schtasks /Create /F /TN "%TASK_NAME%" /SC MINUTE /MO 10 /TR "\"%SCRIPT%\"" /RL LIMITED

if errorlevel 1 (
    echo.
    echo Nije uspelo automatski. Uradi rucno Task Scheduler:
    echo   Program: %SCRIPT%
    echo   Trigger: svakih 10 minuta
    pause
    exit /b 1
)

echo.
echo Zadatak "%TASK_NAME%" kreiran - provera svakih 10 minuta.
echo Za brisanje: schtasks /Delete /TN "%TASK_NAME%" /F
pause
