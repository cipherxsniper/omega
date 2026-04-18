#!/bin/bash

cd ~/Omega

echo "🧠 STARTING OBSERVER (SAFE MODE)"

# WAIT FOR REDIS FIRST
for i in {1..15}; do
  redis-cli ping >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ Redis online"
    break
  fi
  echo "⏳ waiting for redis..."
  sleep 1
done

nohup python3 core/observer.py > logs/observer.log 2>&1 &

echo "🚀 Observer launched"
