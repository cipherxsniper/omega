#!/bin/bash

NODES=5

echo "🌐 STARTING OMEGA SWARM: $NODES NODES"

for i in $(seq 1 $NODES); do
  NODE_ID="python-node-$i"

  NODE_ID=$NODE_ID nohup python3 nodes/node_python.py >> logs/node_$i.log 2>&1 &
  
  echo "🧠 LAUNCHED $NODE_ID"
  sleep 1
done

echo "✅ SWARM ONLINE"
