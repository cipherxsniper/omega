#!/data/data/com.termux/files/usr/bin/bash

echo "[Ω NEXUS v9.1 LAUNCHER] Starting full swarm OS..."

mkdir -p logs

# kill old instances (prevents duplicates)
pkill -f omega_nexus_v9_boot.py
pkill -f omega_neural_bus_v9.py
pkill -f omega_cognitive_mesh_v9.py
pkill -f omega_swarm_balancer_v9_bus.py
pkill -f omega_node_runtime_v9.py
pkill -f omega_chat_assistant_v9_online.py

sleep 1

# ---------------- CORE BUS ----------------
nohup python3 omega_neural_bus_v9.py > logs/bus.log 2>&1 &

# ---------------- COGNITIVE MESH ----------------
nohup python3 omega_cognitive_mesh_v9.py > logs/mesh.log 2>&1 &

# ---------------- SWARM BALANCER ----------------
nohup python3 omega_swarm_balancer_v9_bus.py > logs/balancer.log 2>&1 &

# ---------------- NODE RUNTIME ----------------
nohup python3 omega_node_runtime_v9.py > logs/nodes.log 2>&1 &

# ---------------- BOOT SYSTEM ----------------
nohup python3 omega_nexus_v9_boot.py > logs/nexus.log 2>&1 &

# ---------------- CHAT ASSISTANT (FINAL LAYER) ----------------
nohup python3 omega_chat_assistant_v9_online.py > logs/chat.log 2>&1 &

echo "[Ω NEXUS v9.1 ONLINE]"
echo "[Ω] Bus active"
echo "[Ω] Mesh active"
echo "[Ω] Nodes active"
echo "[Ω] Chat active"
echo "[Ω] System stabilized"
