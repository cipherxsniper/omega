#!/bin/bash

echo "[Ω] Starting Neural Bus System..."

# 1. Start chat
python3 omega_chat_assistant_v9_bus.py &

# 2. Start balancer listener
python3 omega_swarm_balancer_v9_bus.py &

# 3. Start a few nodes
python3 -c "from omega_node_runtime_v9 import node_loop; node_loop('node_1','brain.py')" &
python3 -c "from omega_node_runtime_v9 import node_loop; node_loop('node_2','kernel.py')" &
python3 -c "from omega_node_runtime_v9 import node_loop; node_loop('node_3','memory.py')" &

echo "[Ω] All systems running on neural bus"
wait
