#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 Booting DKF v17 OS Layer..."

source ~/Omega/omega_env/bin/activate

# ensure ollama is alive
pgrep ollama > /dev/null || ollama serve &

sleep 2

python ~/Omega/dkf_v17_os_layer.py
