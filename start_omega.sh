#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 STARTING OMEGA ECOSYSTEM..."

BASE=~/Omega

cd $BASE

# create required folders
mkdir -p logs core node python dashboard memory bus

# =========================
# 1. START REDIS (SAFE)
# =========================
if ! pgrep redis-server > /dev/null; then
  redis-server --daemonize yes
  echo "📡 Redis started"
else
  echo "📡 Redis already running"
fi

# =========================
# 2. CORE ORCHESTRATOR
# =========================
nohup node Omega_v9/omega_v10/core/orchestrator.js > logs/core.log 2>&1 &

# =========================
# 3. NODE WORKERS
# =========================
nohup node Omega_v9/omega_v10/node/worker.js > logs/node.log 2>&1 &

# =========================
# 4. PYTHON SYSTEMS
# =========================
nohup python3 Omega_v9/omega_v10/python/node.py > logs/python.log 2>&1 &

# =========================
# 5. DASHBOARD
# =========================
nohup node Omega_v9/omega_v10/dashboard/server.js > logs/ui.log 2>&1 &

# =========================
# STATUS
# =========================
echo "=================================="
echo "🧠 OMEGA FULL SYSTEM ONLINE"
echo "=================================="

echo "📊 Processes:"
ps aux | grep -E "orchestrator|worker|node.py|redis" | grep -v grep

echo "=================================="
echo "📡 LIVE LOGS READY:"
echo "tail -f ~/Omega/logs/core.log"
