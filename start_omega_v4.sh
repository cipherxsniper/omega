#!/data/data/com.termux/files/usr/bin/bash

echo "[Ω] Starting Omega Core Stack v4..."

nohup python3 ~/Omega/omega_event_bus_v4.py > ~/Omega/omega_bus.log 2>&1 &
sleep 2

nohup python3 ~/Omega/omega_worker_node_v4.py > ~/Omega/omega_worker.log 2>&1 &

echo "[Ω] Omega v4 ONLINE"
