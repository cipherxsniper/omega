#!/bin/bash

cd ~/Omega

redis-server > redis.log 2>&1 &

cd ~/Omega/Omega_v9/omega_v10

mkdir -p logs

nohup node core/orchestrator.js > logs/core.log 2>&1 &
nohup node node/worker.js > logs/node.log 2>&1 &
nohup python3 python/node.py > logs/python.log 2>&1 &
nohup node dashboard/server.js > logs/ui.log 2>&1 &

echo "🧠 Omega v10 FULL SYSTEM ONLINE"
