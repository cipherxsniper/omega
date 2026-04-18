#!/bin/bash

echo "🧠 Omega v34 Unified Boot Starting..."

# 1. FIX REDIS FIRST
pkill redis
redis-server --port 6379 &

sleep 1

# 2. CORE MEMORY
nohup python memory_core.py > logs/memory.log 2>&1 &

# 3. MESSAGE BUS (CRITICAL)
nohup python omega_message_bus_v72.py > logs/bus.log 2>&1 &

# 4. NODE REGISTRY
nohup python omega_v27_registry.py > logs/registry.log 2>&1 &

# 5. SWARM ENGINE
nohup python swarm_engine.py > logs/swarm.log 2>&1 &

# 6. BELIEF / REASONING
nohup python omega_v32_belief_engine.py > logs/belief.log 2>&1 &

# 7. EXECUTION ENGINE
nohup python omega_execution_engine_v7.py > logs/exec.log 2>&1 &

# 8. CORE BRAIN
nohup python app.py > logs/app.log 2>&1 &

# 9. TELEGRAM BOT
nohup python bot.py > logs/bot.log 2>&1 &

# 10. WATCHDOG (LAST)
nohup bash omega_watchdog.sh > logs/watchdog.log 2>&1 &

echo "🧠 Omega v34 ONLINE — all systems launched"
