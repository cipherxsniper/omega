#!/bin/bash

echo "🚀 OMEGA SERVICE STARTING"

# Redis
nohup redis-server > logs/redis.log 2>&1 &

sleep 1

# Observer
nohup python3 core/observer_v18.py > logs/observer.log 2>&1 &

sleep 1

# Node watchdog (auto-restart system)
echo "disabled legacy watchdog"

echo "🧠 OMEGA FULL SYSTEM ONLINE"
