#!/data/data/com.termux/files/usr/bin/bash

echo "[Ω LAUNCHER] Starting Nexus v9 ecosystem..."

# kill old instances first (prevents duplicates)
pkill -f omega_nexus_v9_boot.py
pkill -f omega_neural_bus_v9.py
pkill -f omega_cognitive_mesh_v9.py
pkill -f omega_swarm_balancer_v9_bus.py
pkill -f omega_node_runtime_v9.py

sleep 1

# -----------------------
# CORE SYSTEM
# -----------------------
nohup python3 omega_neural_bus_v9.py > logs/bus.log 2>&1 &
nohup python3 omega_cognitive_mesh_v9.py > logs/mesh.log 2>&1 &

# -----------------------
# SWARM CONTROL
# -----------------------
nohup python3 omega_swarm_balancer_v9_bus.py > logs/balancer.log 2>&1 &
nohup python3 omega_node_runtime_v9.py > logs/nodes.log 2>&1 &

# -----------------------
# BOOT CORE ORCHESTRATOR
# -----------------------
nohup python3 omega_nexus_v9_boot.py > logs/nexus.log 2>&1 &

echo "[Ω] All systems launched in background"
echo "[Ω] Logs: ./logs/"
