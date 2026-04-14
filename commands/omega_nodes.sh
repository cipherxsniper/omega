#!/bin/bash
# commands/omega_nodes.sh
# OmegaOS Multi-Node Manager (Production-Level)

PROJECT_DIR=~/Omega-President/Omega-President
NODES_FILE="$PROJECT_DIR/nodes.json"
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/omega_nodes.log"

mkdir -p "$LOGS_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "===== Omega Node Manager Started ====="

# -------------------------------
# 1. Initialize node registry
# -------------------------------
if [ ! -f "$NODES_FILE" ]; then
    log "nodes.json not found. Creating new registry..."
    echo "[]" > "$NODES_FILE"
fi

# -------------------------------
# 2. Detect active nodes (process-based)
# -------------------------------
log "Scanning for active Omega nodes..."

ACTIVE_NODES=$(ps aux | grep -E "omega_president|quantum_brain|check_nodes.py" | grep -v grep)

if [ -z "$ACTIVE_NODES" ]; then
    log "No active Omega nodes detected."
else
    log "Active nodes detected:"
    echo "$ACTIVE_NODES" | tee -a "$LOG_FILE"
fi

# -------------------------------
# 3. Update node registry (JSON)
# -------------------------------
log "Updating node registry..."

TMP_FILE="$PROJECT_DIR/tmp_nodes.json"
echo "[" > "$TMP_FILE"

INDEX=0
echo "$ACTIVE_NODES" | while read -r line; do
    PID=$(echo $line | awk '{print $2}')
    CMD=$(echo $line | awk '{print $11}')

    echo "  {\"pid\": \"$PID\", \"command\": \"$CMD\", \"status\": \"active\"}," >> "$TMP_FILE"
done

# Remove last comma + close JSON
sed -i '$ s/,$//' "$TMP_FILE"
echo "]" >> "$TMP_FILE"

mv "$TMP_FILE" "$NODES_FILE"

log "Node registry updated → $NODES_FILE"

# -------------------------------
# 4. Auto-healing system
# -------------------------------
log "Running auto-healing checks..."

EXPECTED_NODES=("quantum_brain.py")

for node in "${EXPECTED_NODES[@]}"; do
    if ! pgrep -f "$node" > /dev/null; then
        log "Node missing: $node → Restarting..."

        nohup python3 "$PROJECT_DIR/modules/$node" >> "$LOGS_DIR/${node}.log" 2>&1 &
        
        log "Restarted node: $node"
    else
        log "Node healthy: $node"
    fi
done

# -------------------------------
# 5. Output summary
# -------------------------------
log "===== Node Manager Complete ====="
