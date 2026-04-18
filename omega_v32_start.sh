#!/bin/bash

echo "🧠 OMEGA v32 ADAPTIVE MESH STARTING..."

mkdir -p logs

redis-server --daemonize yes

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ Redis ONLINE"

echo "🧹 Resetting only state..."
redis-cli del omega.nodes.active
redis-cli del omega.consensus.last
redis-cli del omega.consensus.score

echo "🧠 Launching Brain..."
nohup python3 omega_v32_brain.py > logs/brain.log 2>&1 &

echo "📊 Launching Control Center..."
nohup bash omega_v32_control_center.sh > logs/control.log 2>&1 &

echo "🚀 OMEGA v32 ONLINE (ADAPTIVE MESH ACTIVE)"
