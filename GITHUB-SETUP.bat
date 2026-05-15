@echo off
echo.
echo === GitHub Cloud Setup (besplatno 24/7) ===
echo.
echo 1. Otvori: https://github.com/new
echo    Ime: rentvalley-monitor  |  Private: DA
echo.
echo 2. Upload fajlove iz ovog foldera (bez .env):
echo    %~dp0
echo.
echo 3. Settings - Secrets - Actions - dodaj:
echo    TELEGRAM_BOT_TOKEN
echo    TELEGRAM_CHAT_ID
echo.
echo 4. Actions - Rent Valley Monitor - Run workflow
echo.
echo Detaljno: CLOUD-UPUTSTVO.txt
echo.
start https://github.com/new
explorer "%~dp0"
notepad "%~dp0CLOUD-UPUTSTVO.txt"
pause
