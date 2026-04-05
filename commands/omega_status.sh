#!/bin/bash
# commands/omega_status.sh - OmegaOS Professional Status Monitor
# Production-ready, intelligent, multi-node aware, full logging

PROJECT_DIR=~/Omega-President/Omega-President
COMMANDS_DIR="$PROJECT_DIR/commands"
LOGS_DIR="$PROJECT_DIR/logs"
STATUS_LOG="$LOGS_DIR/omega_status.log"
NODES_FILE="$PROJECT_DIR/nodes.json"

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$STATUS_LOG"
}

log "===== OmegaOS Status Check Started ====="

# 1️⃣ Check running Omega processes
log "Checking running Omega processes..."
OMEGA_PROCESSES=$(pgrep -af "quantum_brain.py|omega_.*.sh")
if [[ -z "$OMEGA_PROCESSES" ]]; then
    log "No Omega processes running."
else
    echo "$OMEGA_PROCESSES" | tee -a "$STATUS_LOG"
fi

# 2️⃣ Summary of log files
log "Checking logs summary..."
for file in "$LOGS_DIR"/*.log; do
    if [[ -f "$file" ]]; then
        echo "Log: $(basename "$file") | Size: $(du -h "$file" | cut -f1) | Last Modified: $(stat -c '%y' "$file")" | tee -a "$STATUS_LOG"
    fi
done

# 3️⃣ Check node system (multi-node awareness)
log "Checking Omega nodes..."
if [[ -f "$NODES_FILE" ]]; then
    NODE_COUNT=$(jq '.nodes | length' "$NODES_FILE" 2>/dev/null)
    if [[ $? -eq 0 ]]; then
        log "Detected $NODE_COUNT active node(s)."
        jq -r '.nodes[] | "Node: \(.id) | IP: \(.ip) | Status: \(.status)"' "$NODES_FILE" | tee -a "$STATUS_LOG"
    else
        log "Error reading nodes.json. Check file integrity."
    fi
else
    log "No nodes.json found. Multi-node system inactive."
fi

# 4️⃣ System resource check for Omega modules
log "Checking system resources..."
TOP_INFO=$(top -b -n 1 | head -n 15)
echo "$TOP_INFO" | tee -a "$STATUS_LOG"

log "===== OmegaOS Status Check Completed ====="
