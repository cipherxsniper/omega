#!/bin/bash

echo "🧠 OMEGA CLEAN FOREVER START"

mkdir -p logs

# kill old processes
pkill -f omega_v32 || true

# start redis
redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ REDIS ONLINE"

# start brain safely
nohup python3 omega_v32_brain.py > logs/brain.log 2>&1 &

# start control safely
nohup bash omega_v32_control_center.sh > logs/control.log 2>&1 &

echo "🚀 OMEGA CLEAN SYSTEM ONLINE"

# keep process alive
while true; do
  sleep 10
done
