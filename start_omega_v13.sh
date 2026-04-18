#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 OMEGA v13 STARTING..."

pkill -f node_python.py
pkill -f observer.py

redis-server --daemonize yes

nohup python3 core/observer.py > logs/observer.log 2>&1 &
nohup python3 nodes/node_python.py > logs/node_python.log 2>&1 &

echo "✅ OMEGA v13 ONLINE"
