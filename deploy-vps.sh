#!/bin/bash
set -euo pipefail

# Na VPS-u (Ubuntu): bash deploy-vps.sh
# Pre toga: apt update && apt install -y docker.io docker-compose-plugin git

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "Napravi .env sa TELEGRAM_BOT_TOKEN i TELEGRAM_CHAT_ID"
  cp .env.example .env
  nano .env
  exit 1
fi

docker compose build
docker compose up -d

echo "Monitor radi. Logovi:"
echo "  docker compose logs -f"
