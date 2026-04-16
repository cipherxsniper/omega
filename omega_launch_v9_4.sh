#!/data/data/com.termux/files/usr/bin/bash

mkdir -p logs

echo "[Ω NEXUS v9.4 BOOT]"

nohup python3 kernel/omega_systemd_kernel_v9_4.py > logs/kernel.log 2>&1 &

echo "[Ω SYSTEM LAUNCHED]"
