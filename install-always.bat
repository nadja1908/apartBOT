@echo off
cd /d "%~dp0"

set TASK_LOOP=RentValleyAlwaysOn
set TASK_BACKUP=RentValleyBackup10min
set "VBS=%~dp0run-hidden.vbs"
set "RUNBAT=%~dp0run.bat"

echo.
echo === Rent Valley - uvek ukljucen ===
echo.

schtasks /Delete /TN "%TASK_LOOP%" /F >nul 2>&1
schtasks /Delete /TN "%TASK_BACKUP%" /F >nul 2>&1
schtasks /Delete /TN "RentValleyMonitor" /F >nul 2>&1

echo [1/2] Pokretanje pri svakom loginu (pozadina, svakih 10 min)...
schtasks /Create /F /TN "%TASK_LOOP%" /SC ONLOGON /TR "wscript.exe \"%VBS%\"" /RL LIMITED
if errorlevel 1 goto :fail

echo [2/2] Rezervna provera svakih 10 min (ako loop padne)...
schtasks /Create /F /TN "%TASK_BACKUP%" /SC MINUTE /MO 10 /TR "%RUNBAT%" /RL LIMITED
if errorlevel 1 goto :fail

echo.
echo === Gotovo ===
echo.
echo - Monitor krece kad se ulogujes na Windows
echo - Radi u pozadini (bez crnog prozora)
echo - Provera svakih 10 minuta
echo - PC mora biti upaljen
echo.
echo Pokreni odmah (bez restarta):
echo   wscript.exe "%VBS%"
echo.
choice /C YN /M "Pokreni monitor sada"
if errorlevel 2 goto :end
wscript.exe "%VBS%"
echo Monitor pokrenut u pozadini.
:end
pause
exit /b 0

:fail
echo.
echo Greska. Probaj: desni klik install-always.bat - Run as administrator
pause
exit /b 1
