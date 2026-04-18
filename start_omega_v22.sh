#!/bin/bash

echo "🚀 OMEGA V22 SWARM STARTING"

pkill -f redis
pkill -f observer
pkill -f node

sleep 1

redis-server > logs/redis.log 2>&1 &

sleep 2

nohup python3 core/observer_v22.py > logs/observer.log 2>&1 &

for i in $(seq 1 5); do
  NODE_ID="python-node-$i" nohup python3 nodes/node_python.py > logs/node_$i.log 2>&1 &
done

echo "✅ OMEGA V22 SWARM ONLINE"
