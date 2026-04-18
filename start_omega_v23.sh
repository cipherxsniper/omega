#!/bin/bash

echo "🚀 OMEGA V23 STABLE SWARM START"

# ------------------------
# SAFE SHUTDOWN (CLEAN)
# ------------------------
pkill -f observer_v23.py
pkill -f node_python.py

sleep 2

# ------------------------
# START REDIS FIRST
# ------------------------
echo "📡 Starting Redis..."
redis-server > logs/redis.log 2>&1 &

sleep 3

# ------------------------
# START OBSERVER FIRST
# ------------------------
echo "🧠 Starting Observer v23..."
nohup python3 core/observer_v23.py > logs/observer.log 2>&1 &

sleep 3

# ------------------------
# START NODES (AFTER OBSERVER READY)
# ------------------------
echo "🌐 Starting Nodes..."

for i in $(seq 1 5); do
  NODE_ID="python-node-$i" nohup python3 nodes/node_python.py > logs/node_$i.log 2>&1 &
  sleep 1
done

echo "✅ OMEGA V23 FULLY ONLINE (STABLE MODE)"
