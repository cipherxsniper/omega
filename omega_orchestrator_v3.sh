#!/data/data/com.termux/files/usr/bin/bash

echo ""
echo "🧠🌍🔐 =================================="
echo "   OMEGA ORCHESTRATOR v3"
echo "   AUTONOMOUS SYSTEM KERNEL LAUNCHER"
echo "=================================="
echo ""

cd ~/Omega || exit 1

mkdir -p logs

# =====================================================
# SAFE SHUTDOWN (SCOPED ONLY TO OMEGA RUNTIME LAYERS)
# =====================================================
echo "[V3] Shutting down previous Omega runtime layers..."

pkill -f "runtime_v7/core" >/dev/null 2>&1
pkill -f "test_swarm_emitter" >/dev/null 2>&1
pkill -f "omega_assistant" >/dev/null 2>&1
pkill -f "swarm_bus" >/dev/null 2>&1

sleep 1

# =====================================================
# AUTO DISCOVERY ENGINE (LATEST VERSION PICKER)
# =====================================================

echo "[V3] Detecting latest swarm + memory + assistant layers..."

SWARM_BUS=$(find runtime_v7/core -name "*swarm_bus*.py" 2>/dev/null | sort -V | tail -n 1)

if [ -z "$SWARM_BUS" ]; then
    echo "[V3][ERROR] No Swarm Bus found!"
    exit 1
fi

    echo "[V3][ERROR] No Swarm Bus found!"
    exit 1
fi
EMITTER="runtime_v7/core/test_swarm_emitter.py"
ASSISTANT="runtime_v7/core/omega_assistant_v2.py"

# Memory auto-detect (fallback safe)
MEMORY=$(ls runtime_v7/core/omega_crdt_memory_v*.py 2>/dev/null | sort -V | tail -n 1)

# Safety checks
    echo "[V3][ERROR] No Swarm Bus found!"
    exit 1
fi

if [ -z "$MEMORY" ]; then
    echo "[V3][WARNING] No CRDT memory found — running without persistent memory"
fi

echo "[V3] Swarm Bus    : $SWARM_BUS"
echo "[V3] Memory Core  : $MEMORY"
echo "[V3] Assistant    : $ASSISTANT"

# =====================================================
# START CORE SYSTEMS (DEPENDENCY ORDER)
# =====================================================

echo ""
echo "[V3] Launching MEMORY CORE..."
if [ -n "$MEMORY" ]; then
    nohup python "$MEMORY" > logs/memory.log 2>&1 &
fi

sleep 1

echo "[V3] Launching SWARM BUS..."
nohup python "$SWARM_BUS" > logs/bus.log 2>&1 &

sleep 1

echo "[V3] Launching EVENT EMITTER..."
nohup python "$EMITTER" > logs/emitter.log 2>&1 &

sleep 1

echo "[V3] Launching ASSISTANT LAYER..."
nohup python "$ASSISTANT" > logs/assistant.log 2>&1 &

# =====================================================
# HEALTH MONITOR LOOP (LIGHTWEIGHT TELEMETRY)
# =====================================================

echo ""
echo "🟢 OMEGA ORCHESTRATOR v3 ONLINE"
echo "📡 Swarm Bus   : $SWARM_BUS"
echo "🧠 Memory Core : $MEMORY"
echo "🤖 Assistant   : ACTIVE"
echo ""

HEALTH_COUNTER=0

while true; do
    HEALTH_COUNTER=$((HEALTH_COUNTER + 1))

    echo ""
    echo "────────────────────────────────────"
    echo "🧠 [V3 HEALTH CHECK #$HEALTH_COUNTER]"
    echo "Time: $(date +%H:%M:%S)"

    # Process visibility checks
    echo "[CHECK] Swarm Bus:"
    pgrep -f "swarm_bus" >/dev/null && echo "  ✅ RUNNING" || echo "  ❌ DOWN"

    echo "[CHECK] Memory:"
    pgrep -f "omega_crdt" >/dev/null && echo "  ✅ RUNNING" || echo "  ⚠️ NOT DETECTED"

    echo "[CHECK] Assistant:"
    pgrep -f "assistant" >/dev/null && echo "  ✅ RUNNING" || echo "  ❌ DOWN"

    echo "────────────────────────────────────"

    sleep 10
done
