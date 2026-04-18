#!/bin/bash

echo "🧠 OMEGA V32 ISOLATED BOOT"

pkill -f omega || true
pkill -f python3 || true

mkdir -p logs

# REDIS
redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ REDIS READY"

# CORE SYSTEM
nohup python3 omega_v32_brain.py > logs/brain.log 2>&1 &
nohup bash omega_v32_control_center.sh > logs/control.log 2>&1 &

echo "🚀 SYSTEM ONLINE"

# MASTER KEEP ALIVE LOOP (THIS FIXES YOUR ISSUE)
while true; do
  echo "🧠 system alive $(date)"
  sleep 10
done
