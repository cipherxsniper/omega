#!/bin/bash

echo "🧠 STARTING OMEGA ECOSYSTEM..."

cd ~/Omega/Omega_v9/omega_v10 || exit

mkdir -p logs

# Start Redis (if not already running)
redis-server --daemonize yes 2>/dev/null

# CORE ORCHESTRATOR
node core/orchestrator.js > logs/core.log 2>&1 &

# NODE WORKERS
node node/node_worker.js > logs/node.log 2>&1 &

# PYTHON BRAIN
python3 python/python_node.py > logs/python.log 2>&1 &

# OBSERVER (English translator)
python3 ~/Omega/omega_observer.py > logs/observer.log 2>&1 &

echo "✅ OMEGA FULL SYSTEM ONLINE"
echo "📡 ATTACHING LIVE INTELLIGENCE FEED..."
