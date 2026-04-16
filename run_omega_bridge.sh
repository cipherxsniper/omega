#!/data/data/com.termux/files/usr/bin/bash

cd ~/Omega
echo "[Ω BOOT] Starting Omega Integration Bridge..."

while true; do
    python3 omega_integration_bridge_v4_1_v2.py
    sleep 2
done
