#!/bin/bash

mkdir -p logs

while true; do
  COUNT=$(ps aux | grep observer_v27_node.py | grep -v grep | wc -l)

  if [ "$COUNT" -lt 3 ]; then
    echo "⚡ Node deficit detected: spawning nodes..."
    nohup python3 observer_v27_node.py > logs/node_auto.log 2>&1 &
  fi

  sleep 3
done
