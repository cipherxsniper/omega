#!/data/data/com.termux/files/usr/bin/bash

cd ~/Omega

echo "🧠 OMEGA BOOTSTRAP v1 INITIATING..."

# -------------------------
# 1. ENSURE DIRECTORY STRUCTURE
# -------------------------
mkdir -p core python node dashboard logs bus memory tools

# -------------------------
# 2. CHECK REDIS
# -------------------------
if ! pgrep redis-server > /dev/null; then
    echo "📡 Starting Redis..."
    redis-server --daemonize yes
else
    echo "📡 Redis already running"
fi

# -------------------------
# 3. VALIDATE CORE FILES
# -------------------------
CORE_MISSING=0

[ ! -f core/event_bus.js ] && CORE_MISSING=1
[ ! -f core/observer.js ] && CORE_MISSING=1

if [ $CORE_MISSING -eq 1 ]; then
    echo "⚠️ Core modules missing — system may be degraded"
fi

# -------------------------
# 4. START SYSTEM SERVICES
# -------------------------

echo "🚀 Launching Omega Core..."

nohup node core/observer.js > logs/observer.log 2>&1 &
nohup node core/heartbeat.js node-js-1 > logs/js.log 2>&1 &
nohup python3 python/heartbeat.py > logs/python.log 2>&1 &

# -------------------------
# 5. SYSTEM STATUS REPORT
# -------------------------

echo ""
echo "🧠 OMEGA BOOT COMPLETE"
echo "----------------------"

echo "📊 Active Processes:"
ps aux | grep -E "observer|heartbeat|redis" | grep -v grep

echo ""
echo "📡 Observer Log:"
echo "tail -f ~/Omega/logs/observer.log"

echo ""
echo "🧠 SYSTEM READY"
