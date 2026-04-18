#!/bin/bash

echo "🧠 Starting Omega v9..."

pkill -f app.py
pkill -f bot.py

nohup python app.py > brain.log 2>&1 &
sleep 2

nohup python bot.py > bot.log 2>&1 &

echo "✅ Omega v9 running in background"
