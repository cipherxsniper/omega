#!/data/data/com.termux/files/usr/bin/bash

mkdir -p logs

echo "[Ω NEXUS v9.2 LAUNCH]"

nohup python3 omega_neural_bus_v9.py > logs/bus.log 2>&1 &
nohup python3 omega_cognitive_mesh_v9.py > logs/mesh.log 2>&1 &
nohup python3 omega_swarm_balancer_v9_bus.py > logs/balancer.log 2>&1 &
nohup python3 omega_node_runtime_v9.py > logs/nodes.log 2>&1 &
nohup python3 omega_chat_assistant_v9_online.py > logs/chat.log 2>&1 &
nohup python3 omega_nexus_v9_2_kernel.py > logs/kernel.log 2>&1 &

echo "[Ω NEXUS v9.2 ONLINE]"
