#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 STOPPING OMEGA..."

pkill -f app.py
pkill -f bot.py
pkill redis-server

echo "🛑 OMEGA STOPPED"
