#!/bin/bash

cd "$(dirname "$0")"

echo "🧠 OMEGA v11 SELF-HEALING LAUNCHER STARTING..."

source venv/bin/activate

LOG_DIR=logs
mkdir -p $LOG_DIR

start_flask() {
  while true; do
    echo "🧠 Starting Flask Brain..."
    python app.py >> $LOG_DIR/flask.log 2>&1
    echo "⚠️ Flask crashed — restarting in 2s..."
    sleep 2
  done
}

start_bot() {
  while true; do
    echo "🤖 Starting Telegram Bot..."
    python bot.py >> $LOG_DIR/bot.log 2>&1
    echo "⚠️ Bot crashed — restarting in 2s..."
    sleep 2
  done
}

# Run both in background
start_flask &
start_bot &

echo "✅ OMEGA v11 ONLINE (SELF-HEALING MODE)"
echo "📦 Logs: ./logs/"
echo "🧠 System is now autonomous"

wait
