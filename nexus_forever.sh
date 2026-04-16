#!/data/data/com.termux/files/usr/bin/bash

export PYTHONPATH=$HOME/Omega

while true; do
    echo "[NEXUS] booting cluster..."
    
    python omega_cluster_v9_6.py

    echo "[NEXUS] cluster stopped — restarting in 2s..."
    sleep 2
done
