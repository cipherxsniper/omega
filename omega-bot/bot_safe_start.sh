#!/data/data/com.termux/files/usr/bin/bash

cd ~/Omega/omega-bot

echo "🤖 Starting safe bot..."

pkill -f bot.py

nohup python bot.py > bot.log 2>&1 &

echo "✅ Bot running safely in background"
