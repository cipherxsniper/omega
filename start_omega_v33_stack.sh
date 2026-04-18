#!/bin/bash

echo "🧠 Omega Ecosystem Booting..."

redis-server &

sleep 1

nohup python omega_supervisor_v27.sh > logs/supervisor.log 2>&1 &
nohup python omega_bus.py > logs/bus.log 2>&1 &
nohup python memory_core.py > logs/memory.log 2>&1 &
nohup python omega_kernel_v33.py > logs/brain.log 2>&1 &
nohup python swarm_engine.py > logs/swarm.log 2>&1 &
nohup python node_scanner.py > logs/scanner.log 2>&1 &

nohup python app.py > logs/app.log 2>&1 &
nohup python bot.py > logs/bot.log 2>&1 &

nohup bash omega_watchdog.sh > logs/watchdog.log 2>&1 &

echo "🧠 Omega Ecosystem FULLY ONLINE"
