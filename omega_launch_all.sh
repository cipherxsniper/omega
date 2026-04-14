#!/data/data/com.termux/files/usr/bin/bash

echo "[OMEGA] MASTER FEDERATION BOOTING..."

# Core cognition layers
nohup python omega_kernel_v40.py > logs/v40.log 2>&1 &
nohup python omega_kernel_v41.py > logs/v41.log 2>&1 &
nohup python omega_kernel_v42.py > logs/v42.log 2>&1 &
nohup python omega_v55_civilization_v1.py > logs/v55.log 2>&1 &
nohup python omega_v56_identity_core.py > logs/v56.log 2>&1 &
nohup python omega_v57_cognitive_society.py > logs/v57.log 2>&1 &
nohup python omega_v59_specialization.py > logs/v59.log 2>&1 &
nohup python omega_v62_cognitive_physics.py > logs/v62.log 2>&1 &

echo "[OMEGA] ALL SYSTEMS LAUNCHED"
echo "[OMEGA] Logs stored in ./logs/"
