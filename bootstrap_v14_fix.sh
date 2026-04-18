#!/bin/bash

echo "🧠 OMEGA v14 BOOTSTRAP FIX STARTING..."

cd ~/Omega || exit 1

# -------------------------
# 1. SAFE DIRECTORY LAYER
# -------------------------
mkdir -p core memory logs nodes runtime bus

# -------------------------
# 2. SAFE MEMORY FILES
# -------------------------
if [ ! -f memory/omega_memory_v13.json ]; then
  echo '{"events":[],"nodes":{},"scores":{}}' > memory/omega_memory_v13.json
fi

if [ ! -f memory/omega_registry.json ]; then
  echo '{"nodes":{},"active":0}' > memory/omega_registry.json
fi

# -------------------------
# 3. CLEAN OLD PROCESSES
# -------------------------
pkill -f omega_observer.py 2>/dev/null
pkill -f node_python.py 2>/dev/null
pkill -f redis-server 2>/dev/null

# -------------------------
# 4. START REDIS
# -------------------------
redis-server --daemonize yes

# -------------------------
# 5. START OBSERVER (SAFE)
# -------------------------
nohup python3 core/observer.py > logs/observer.log 2>&1 &

sleep 1

echo "🧠 OMEGA v14 FIX BOOT COMPLETE"
echo "📊 Checking logs..."
tail -n 20 logs/observer.log
