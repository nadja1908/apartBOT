$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "=== Rent Valley Listing Monitor - Setup ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Biblioteke..."
$pipOk = $false
try {
    python -c "import requests, dotenv" 2>$null
    if ($LASTEXITCODE -eq 0) { $pipOk = $true }
} catch {}

if ($pipOk) {
    Write-Host "      Vec instalirano - preskacem pip" -ForegroundColor Green
} else {
    Write-Host "      Instaliram (moze potrajati 1-2 min)..."
    python -m pip install requests python-dotenv --timeout 60
    Write-Host "      OK" -ForegroundColor Green
}

if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "[2/4] Telegram podesavanje" -ForegroundColor Yellow
    Write-Host "Token: @BotFather -> /newbot"
    Write-Host "Chat ID: @userinfobot ili getUpdates"
    Write-Host ""
    $token = Read-Host "TELEGRAM_BOT_TOKEN"
    $chatId = Read-Host "TELEGRAM_CHAT_ID"
    $envContent = "TELEGRAM_BOT_TOKEN=$token`nTELEGRAM_CHAT_ID=$chatId"
    [System.IO.File]::WriteAllText("$PSScriptRoot\.env", $envContent)
    Write-Host "      .env sacuvan" -ForegroundColor Green
} else {
    Write-Host "[2/4] .env vec postoji" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/4] Seed oglasa..."
python monitor.py --seed

Write-Host ""
Write-Host "[4/4] Test Telegram..."
python monitor.py --test

Write-Host ""
Write-Host "=== Gotovo ===" -ForegroundColor Green
Write-Host "Novi oglasi: dupli klik run.bat"
Write-Host ""
