#!/bin/bash

echo "🚀 OMEGA v24 EMERGENT SWARM START"

pkill -f observer_v24.py
pkill -f node_python.py

sleep 2

redis-server > logs/redis.log 2>&1 &

sleep 3

nohup python3 core/observer_v24.py > logs/observer.log 2>&1 &

sleep 2

for i in $(seq 1 5); do
  NODE_ID="python-node-$i" nohup python3 nodes/node_python.py > logs/node_$i.log 2>&1 &
  sleep 1
done

echo "✅ OMEGA v24 ONLINE"
