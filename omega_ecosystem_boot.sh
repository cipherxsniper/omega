#!/data/data/com.termux/files/usr/bin/bash

echo ""
echo "🧠🌍🔐 ==============================="
echo "   OMEGA ECOSYSTEM BOOT v1"
echo "   AUTONOMOUS SYSTEM LAUNCHER"
echo "==============================="
echo ""

cd ~/Omega || exit

mkdir -p logs

# -----------------------------
# KILL OLD SYSTEMS CLEANLY
# -----------------------------
echo "[BOOT] Stopping existing Omega processes..."
pkill -f omega_ >/dev/null 2>&1
pkill -f runtime_v7 >/dev/null 2>&1
pkill -f swarm >/dev/null 2>&1

sleep 1

# -----------------------------
# CORE DECISION: USE LATEST SYSTEMS
# -----------------------------
echo "[BOOT] Launching CORE MEMORY + SWARM + COGNITION..."

# MEMORY CORE (latest CRDT / shared memory)
MEMORY_CORE="omega_crdt_memory_v4.py"

# SWARM BUS (latest v14+ you’re using)
SWARM_BUS="runtime_v7/core/v9_9_swarm_bus_v14.py"

# EMITTER (signal generator)
EMITTER="runtime_v7/core/test_swarm_emitter.py"

# ASSISTANT (interface layer)
ASSISTANT="runtime_v7/core/omega_assistant_v2.py"

# SEMANTIC LAYER (if exists)
SEMANTIC="runtime_v7/core/omega_semantic_engine_v1.py"

# -----------------------------
# START CORE SYSTEMS
# -----------------------------

echo "[BOOT] Starting Memory Core..."
nohup python $MEMORY_CORE > logs/memory_core.log 2>&1 &

sleep 1

echo "[BOOT] Starting Swarm Bus..."
nohup python $SWARM_BUS > logs/bus.log 2>&1 &

sleep 1

echo "[BOOT] Starting Emitter..."
nohup python $EMITTER > logs/emitter.log 2>&1 &

sleep 1

echo "[BOOT] Starting Assistant..."
nohup python $ASSISTANT > logs/assistant.log 2>&1 &

sleep 1

# -----------------------------
# OPTIONAL: SEMANTIC LAYER
# -----------------------------
if [ -f "$SEMANTIC" ]; then
    echo "[BOOT] Starting Semantic Layer..."
    nohup python $SEMANTIC > logs/semantic.log 2>&1 &
fi

# -----------------------------
# LIVE STATUS MONITOR
# -----------------------------
echo ""
echo "🟢 OMEGA ECOSYSTEM ONLINE"
echo "📡 Bus: $SWARM_BUS"
echo "🧠 Memory: $MEMORY_CORE"
echo "🤖 Assistant: $ASSISTANT"
echo ""

# simple heartbeat monitor
while true; do
    echo "[$(date +%H:%M:%S)] Omega ecosystem running..."
    sleep 10
done
