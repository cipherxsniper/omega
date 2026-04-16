#!/data/data/com.termux/files/usr/bin/bash

echo "[Ω] scanning Omega runtime systems..."

cd ~/Omega || exit

# kill existing omega processes
pkill -f run_v7 || true

# pick latest run_v7*.py file
LATEST=$(ls -1 run_v7*_system.py 2>/dev/null | sort -V | tail -n 1)

if [ -z "$LATEST" ]; then
    echo "[Ω] No run_v7 system found."
    exit 1
fi

echo "[Ω] launching: $LATEST"

PYTHONUNBUFFERED=1 nohup python -u "$LATEST" \
> omega_master.log 2>&1 &

echo "[Ω] running in background"
echo "[Ω] log: tail -f ~/Omega/omega_master.log"
