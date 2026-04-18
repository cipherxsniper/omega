#!/bin/bash

mkdir -p logs

echo "📡 Starting Redis..."

redis-server --daemonize yes

sleep 1

echo "⏳ Waiting for Redis..."
until redis-cli ping >/dev/null 2>&1
do
    sleep 1
done

echo "✅ Redis ONLINE"

echo "🧠 Starting Omega Nodes..."

nohup bash omega_supervisor_v26.sh > logs/node1.log 2>&1 &
nohup bash omega_supervisor_v26.sh > logs/node2.log 2>&1 &
nohup bash omega_supervisor_v26.sh > logs/node3.log 2>&1 &

echo "✅ Omega V26 SELF-HEALING CLUSTER ONLINE"

# 🔥 KEEP SCRIPT ALIVE (THIS WAS MISSING)
wait
