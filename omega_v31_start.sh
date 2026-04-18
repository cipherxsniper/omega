#!/bin/bash

source omega_v31_lock.sh

echo "🧠 OMEGA v31 SAFE START"

mkdir -p logs

echo "⏳ Starting Redis..."
redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ Redis ONLINE"

echo "🧹 Resetting registry ONLY (NOT killing processes)..."
redis-cli del omega.nodes.active
redis-cli del omega.consensus.last
redis-cli del omega.consensus.score

echo "🧠 Starting Brain..."
nohup python3 omega_v31_brain.py > logs/brain.log 2>&1 &

sleep 2

echo "⚙️ Starting Watchdog..."
echo "disabled legacy watchdog"

sleep 2

echo "📊 Starting Control Center..."
nohup bash omega_v31_control_center.sh > logs/control.log 2>&1 &

echo "🚀 OMEGA v31 STABLE ONLINE"
