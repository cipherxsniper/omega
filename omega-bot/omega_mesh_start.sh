#!/bin/bash

echo "🧠 STARTING OMEGA MESH..."

# start redis (if not running)
pgrep redis-server >/dev/null || redis-server > redis.log 2>&1 &

# start brain
nohup python app.py > brain.log 2>&1 &

sleep 2

# start bot
nohup python bot.py > bot.log 2>&1 &

echo "✅ OMEGA SERVICE MESH ONLINE"
echo "🧠 Brain + Bot running in background"
