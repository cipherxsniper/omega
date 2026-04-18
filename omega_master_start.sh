#!/data/data/com.termux/files/usr/bin/bash

# ============================
# 🚀 OMEGA MASTER SUPERVISOR
# ============================

BASE_DIR="$PWD"
LOG_DIR="$BASE_DIR/logs"

mkdir -p "$LOG_DIR"

echo "🚀 OMEGA MASTER STARTING..."

# ----------------------------
# 1. START REDIS IF NOT RUNNING
# ----------------------------
if ! pgrep -x "redis-server" > /dev/null; then
    echo "📡 Starting Redis..."
    redis-server --daemonize yes
else
    echo "📡 Redis already running"
fi

# ----------------------------
# 2. FUNCTION: START PROCESS WITH RESTART LOOP
# ----------------------------
start_service() {
    NAME=$1
    CMD=$2
    LOG=$3

    while true; do
        echo "🧠 STARTING $NAME"
        eval "$CMD >> $LOG 2>&1"
        echo "⚠️ $NAME CRASHED - RESTARTING IN 2s"
        sleep 2
    done
}

# ----------------------------
# 3. OBSERVER v24
# ----------------------------
start_service "OBSERVER_V24" \
"python3 core/observer_v24.py" \
"$LOG_DIR/observer.log" &

# ----------------------------
# 4. SWARM NODES (5)
# ----------------------------
start_service "NODE_1" \
"NODE_ID=python-node-1 python3 nodes/node_python.py" \
"$LOG_DIR/node_1.log" &

start_service "NODE_2" \
"NODE_ID=python-node-2 python3 nodes/node_python.py" \
"$LOG_DIR/node_2.log" &

start_service "NODE_3" \
"NODE_ID=python-node-3 python3 nodes/node_python.py" \
"$LOG_DIR/node_3.log" &

start_service "NODE_4" \
"NODE_ID=python-node-4 python3 nodes/node_python.py" \
"$LOG_DIR/node_4.log" &

start_service "NODE_5" \
"NODE_ID=python-node-5 python3 nodes/node_python.py" \
"$LOG_DIR/node_5.log" &

# ----------------------------
# 5. REINFORCEMENT LEARNING LOOP
# ----------------------------
start_service "RL_ENGINE_V10" \
"bash run_omega_v10.sh" \
"$LOG_DIR/v10_forever.log" &

# ----------------------------
# 6. WATCHDOG (optional extra layer)
# ----------------------------
start_service "WATCHDOG" \
"bash core/node_watchdog.sh" \
"$LOG_DIR/watchdog.log" &

echo "✅ OMEGA MASTER ONLINE"
echo "🧠 All systems running under supervisor loops"

# Keep script alive
while true; do
    sleep 60
done
