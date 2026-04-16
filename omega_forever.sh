#!/data/data/com.termux/files/usr/bin/bash

echo "[Ω NEXUS FOREVER START]"

mkdir -p logs

nohup python omega_nexus_v9_boot.py > logs/nexus.log 2>&1 &
nohup python omega_neural_bus_v9.py > logs/bus.log 2>&1 &
nohup python omega_cognitive_mesh_v9.py > logs/mesh.log 2>&1 &
nohup python omega_swarm_balancer_v9_bus.py > logs/balancer.log 2>&1 &
nohup python omega_node_runtime_v9.py > logs/runtime.log 2>&1 &
nohup python omega_chat_assistant_v9_online.py > logs/chat.log 2>&1 &

echo "[Ω SYSTEM ONLINE]"
