@echo off
schtasks /Delete /TN "RentValleyAlwaysOn" /F >nul 2>&1
schtasks /Delete /TN "RentValleyBackup10min" /F >nul 2>&1
schtasks /Delete /TN "RentValleyMonitor" /F >nul 2>&1
call "%~dp0stop-monitor.bat"
