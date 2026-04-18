#!/bin/bash

echo "🧠 OMEGA V32 MASTER CONTROLLER"

pkill -f omega_v32_brain.py || true

mkdir -p logs

redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ Redis ONLINE"

# 🔥 FIX: -u forces unbuffered output
python3 -u omega_v32_brain.py > logs/brain.log 2>&1 &
BRAIN_PID=$!

echo "🧠 Brain PID: $BRAIN_PID"

while true; do
  if ! kill -0 $BRAIN_PID 2>/dev/null; then
    echo "⚠️ Brain died — restarting..."
    python3 -u omega_v32_brain.py > logs/brain.log 2>&1 &
    BRAIN_PID=$!
  fi

  sleep 2
done
