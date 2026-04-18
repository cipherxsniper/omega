#!/bin/bash

echo "🧠 Starting Omega Full System..."

# kill old instances
pkill -f app.py
pkill -f bot.py
pkill redis-server

# start redis in background
redis-server > redis.log 2>&1 &
sleep 2

# start brain in background
nohup python app.py > brain.log 2>&1 &
sleep 3

# start bot in background
nohup python bot.py > bot.log 2>&1 &

echo "✅ Omega is ONLINE"
echo "📡 Brain: http://127.0.0.1:5000"
echo "🤖 Bot: running via Telegram"
