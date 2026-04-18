#!/bin/bash

nohup python3 omega_mesh_bus_v1.py > mesh_bus.log 2>&1 &

nohup python3 wink_wink_brain_v24.py > v24.log 2>&1 &
nohup python3 wink_wink_brain_v25.py > v25.log 2>&1 &
nohup python3 wink_wink_brain_v28.py > v28.log 2>&1 &

echo "🧠 SWARM RUNNING IN BACKGROUND"
