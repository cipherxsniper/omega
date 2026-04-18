#!/bin/bash

echo "🚀 OMEGA V20 FULL BOOT"

# 1. Redis FIRST
nohup redis-server > logs/redis.log 2>&1 &
sleep 2

# 2. Observer
nohup python3 core/observer_v20.py > logs/observer.log 2>&1 &
sleep 2

# 3. Swarm nodes
bash core/swarm_launcher_v20.sh

echo "🧠 OMEGA V20 ONLINE"
