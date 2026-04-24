#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 Starting DKF System..."

source ~/Omega/omega_env/bin/activate

nohup ollama serve > ~/ollama.log 2>&1 &

sleep 3

python ~/Omega/dkf_core_runner.py
