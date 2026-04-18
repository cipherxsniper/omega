#!/bin/bash

echo "🧠 OMEGA v15 BOOT SEQUENCE"

bash core/redis_daemon_safe.sh

python3 fix_registry_boot.py

nohup python3 core/observer_safe.py > logs/observer.log 2>&1 &

nohup python3 nodes/node_python.py > logs/node_python.log 2>&1 &

echo "🧠 OMEGA v15 ONLINE"

echo "📊 LIVE OBSERVER:"
tail -f logs/observer.log
