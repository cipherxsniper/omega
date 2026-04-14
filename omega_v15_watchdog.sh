#!/bin/bash

while true; do
    echo "[WATCHDOG] Starting Omega v15..."
    python run_omega_v15.py

    echo "[WATCHDOG] Omega crashed. Restarting in 3 seconds..."
    sleep 3
done
