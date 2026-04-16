#!/bin/bash

cd ~/Omega

mkdir -p logs

echo "🧠 Starting Omega Ecosystem..."

# CORE SYSTEM
node Omega/Omega_v9/omega_v10/core/orchestrator.js > logs/core.log 2>&1 &

# WORKERS (SAFE CHECKS)
if [ -f Omega/Omega_v9/omega_v10/node/worker.js ]; then
  node Omega/Omega_v9/omega_v10/node/worker.js > logs/node.log 2>&1 &
fi

if [ -f Omega/Omega_v9/omega_v10/python/node.py ]; then
  python3 Omega/Omega_v9/omega_v10/python/node.py > logs/python.log 2>&1 &
fi

echo "🧠 OMEGA SYSTEM STARTED"
