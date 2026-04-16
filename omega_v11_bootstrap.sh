#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/Omega
cd $BASE || exit 1

echo "🧠 OMEGA v11 BOOTSTRAP STARTING..."

# kill old duplicates
pkill -f heartbeat
pkill -f observer
pkill -f orchestrator

# ensure redis
pgrep redis-server >/dev/null || redis-server --daemonize yes

# =========================
# 1. START REGISTRY CORE
# =========================
node core/registry.js > logs/registry.log 2>&1 &
echo "📦 Registry ONLINE"

# =========================
# 2. START EVENT BUS
# =========================
node core/event_bus.js > logs/events.log 2>&1 &
echo "📡 Event Bus ONLINE"

# =========================
# 3. START OBSERVER (translator layer)
# =========================
node core/observer.js > logs/observer.log 2>&1 &
echo "🧠 Observer ONLINE"

# =========================
# 4. START NODES
# =========================
python3 python/heartbeat.py > logs/python.log 2>&1 &
node core/heartbeat.js node-js-1 > logs/node.log 2>&1 &

echo ""
echo "✅ OMEGA v11 FULL SYSTEM ONLINE"
echo "------------------------------"
echo "Registry: ACTIVE"
echo "Event Bus: ACTIVE"
echo "Observer: ACTIVE"
echo "Nodes: INITIALIZED"
echo "------------------------------"

tail -f logs/observer.log
