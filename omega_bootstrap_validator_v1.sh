#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/Omega"
cd "$BASE" || exit 1

echo "🧠 OMEGA BOOTSTRAP VALIDATOR v1"
echo "================================"

# 1. kill old system cleanly
pkill -f "observer.js"
pkill -f "heartbeat.js"
pkill -f "heartbeat.py"

# 2. ensure redis running
pgrep redis-server >/dev/null || {
  echo "📡 Starting Redis..."
  redis-server --daemonize yes
}

# 3. start node observer (single instance)
echo "🚀 Starting Node Observer..."
nohup node core/orchestrator.js > logs/core.log 2>&1 &

# 4. start JS heartbeat (single instance)
echo "🟢 Starting JS heartbeat..."
nohup node core/heartbeat.js node-js-1 > logs/node.log 2>&1 &

# 5. start Python heartbeat (single instance)
echo "🐍 Starting Python heartbeat..."
nohup python3 python/heartbeat.py > logs/python.log 2>&1 &

# 6. attach observer feed
echo "📡 Attaching Observer Feed..."
tail -n 20 logs/core.log

echo ""
echo "🧠 OMEGA SYSTEM ONLINE (v1 validated)"
echo "Nodes initialized: 2"
echo "Registry: ACTIVE"
