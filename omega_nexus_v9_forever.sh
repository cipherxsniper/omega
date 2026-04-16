#!/data/data/com.termux/files/usr/bin/bash

BASE="/data/data/com.termux/files/home/Omega"
LOG="$BASE/logs"

mkdir -p "$LOG"

echo "[Ω NEXUS v9 FOREVER LAUNCH]"

start() {
  NAME=$1
  FILE=$2
  nohup python3 "$BASE/$FILE" > "$LOG/$NAME.log" 2>&1 &
  echo "[Ω STARTED] $FILE"
}

start nexus     omega_nexus_v9_boot.py
start bus       omega_neural_bus_v9.py
start mesh      omega_cognitive_mesh_v9.py
start balancer  omega_swarm_balancer_v9_bus.py
start runtime   omega_node_runtime_v9.py
start chat      omega_chat_assistant_v9_online.py

echo "[Ω SYSTEM ONLINE]"
