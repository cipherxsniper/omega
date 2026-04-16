#!/bin/bash

cd ~/Omega/Omega_v9
mkdir -p logs

nohup node core/orchestrator.js > logs/core.log 2>&1 &
nohup node node/node_worker.js > logs/node.log 2>&1 &
nohup python3 python/python_node.py > logs/python.log 2>&1 &

echo "🧠 Omega v9 FULL SWARM ONLINE"
