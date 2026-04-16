#!/data/data/com.termux/files/usr/bin/bash

VERSION=$1

echo "[Ω] Switching Omega to version: $VERSION"

pkill -f omega_worker_node.py

sleep 2

bash ~/Omega/start_omega_${VERSION}.sh
