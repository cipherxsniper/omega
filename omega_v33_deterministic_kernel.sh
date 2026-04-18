#!/bin/bash

echo "🧠 OMEGA v33 DETERMINISTIC KERNEL STARTING"

mkdir -p logs

# ----------------------------
# CLEAN STATE
# ----------------------------
pkill -f omega_v32 || true
pkill -f omega_v33 || true

# ----------------------------
# REDIS CORE
# ----------------------------
redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ REDIS READY (v33 CORE)"

# ----------------------------
# START BRAIN (DETERMINISTIC PID CONTROL)
# ----------------------------
start_brain() {
  nohup python3 omega_v32_brain.py > logs/brain.log 2>&1 &
  echo $! > logs/brain.pid
}

start_brain

# ----------------------------
# DETERMINISTIC SUPERVISOR LOOP
# ----------------------------
while true; do

  PID=$(cat logs/brain.pid 2>/dev/null)

  # Validate process existence
  if ! kill -0 "$PID" 2>/dev/null; then
    echo "⚠️ BRAIN LOST — RESTARTING DETERMINISTICALLY"
    start_brain
  fi

  # HEALTH CHECK SIGNAL
  echo "🧠 v33 kernel alive | brain_pid=$PID | time=$(date)"

  sleep 2
done
