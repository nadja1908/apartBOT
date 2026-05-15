@echo off
cd /d "%~dp0"
echo.
echo === Brzi setup (bez pip) ===
echo.

if not exist .env (
    echo Kopiraj .env.example u .env i popuni TOKEN i CHAT_ID
    copy .env.example .env
    notepad .env
    echo.
    echo Sacuvaj .env u Notepad-u i pritisni Enter ovde...
    pause
)

python monitor.py --seed
python monitor.py --test
echo.
pause
