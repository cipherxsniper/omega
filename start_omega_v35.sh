#!/bin/bash

echo "🧠 Omega v35 Unified Cognition Kernel Boot"

# CORE MEMORY FIRST
nohup python omega_truth_memory_v35.py &
nohup python memory_core.py &

# MESSAGE BUS
nohup python omega_message_bus_v72.py &

# NODE REGISTRY
nohup python omega_v27_registry.py &

# SWARM
nohup python swarm_engine.py &

# APP CORE
nohup python app.py &

# BOT
nohup python bot.py &

# SELF REPAIR LOOP
nohup bash omega_self_repair_v35.sh &

echo "🧠 Omega v35 ONLINE — unified memory layer active"
