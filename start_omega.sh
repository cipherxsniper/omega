#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 STARTING OMEGA v13 NEURAL CORE..."

nohup python3 ~/Omega/omega_bootstrap_v13.py > ~/Omega/logs/v13.log 2>&1 &

echo "✅ OMEGA v13 RUNNING (embedding + reinforcement + memory training)"
