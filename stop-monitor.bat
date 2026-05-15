@echo off
echo Gasim Rent Valley monitor...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Rent Valley*" >nul 2>&1
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "listing-monitor\\monitor.py" >nul && taskkill /F /PID %%a >nul 2>&1
)
schtasks /End /TN "RentValleyAlwaysOn" >nul 2>&1
echo Gotovo. Za trajno iskljucenje:
echo   uninstall-always.bat
pause
