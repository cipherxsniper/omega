#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 DKF v16 CONTROL SYSTEM BOOTING..."

source ~/Omega/omega_env/bin/activate

# start ollama if not running
pgrep ollama > /dev/null || ollama serve &

sleep 3

# start control plane in background
nohup python ~/Omega/dkf_v16_control_plane.py > ~/dkf_control.log 2>&1 &

# start runtime chat
python ~/Omega/dkf_v16_runtime_bridge.py
