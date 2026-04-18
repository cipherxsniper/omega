#!/bin/bash

echo "🧠 LAUNCHING WINK WINK SWARM"

python3 omega_mesh_bus_v1.py &

python3 wink_wink_brain_v24.py &
python3 wink_wink_brain_v25.py &
python3 wink_wink_brain_v28.py &

echo "🧠 SWARM ONLINE"
wait
