#!/bin/bash

mkdir -p logs

while true; do
  echo "🧠 Starting brain..."

  python3 swarm_brain_v27.py >> logs/brain.log 2>&1

  echo "⚠️ Brain crashed — restarting in 2s..."
  sleep 2
done
