#!/bin/bash

while true; do
  echo "🧠 NODE WATCHDOG STARTING NODE..."
  nohup python3 nodes/node_python.py >> logs/node_python.log 2>&1
  echo "⚠️ NODE CRASHED — RESTARTING IN 2s..."
  sleep 2
done
