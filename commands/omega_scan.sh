#!/bin/bash
# omega_scan.sh
# Fully intelligent IoT + node scanning for production-level OmegaOS

LOG_FILE="$HOME/Omega-President/Omega-President/logs/omega_scan.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] ===== Omega Scan Started =====" | tee -a $LOG_FILE

# 1. List running Omega nodes
echo "[$DATE] Scanning for Omega nodes..." | tee -a $LOG_FILE
NODE_PROCESSES=$(ps aux | grep -E 'omega_president|check_nodes.py' | grep -v grep)
if [ -z "$NODE_PROCESSES" ]; then
    echo "[$DATE] No active Omega nodes found." | tee -a $LOG_FILE
else
    echo "$NODE_PROCESSES" | tee -a $LOG_FILE
fi

# 2. Scan Wi-Fi networks
echo "[$DATE] Scanning for Wi-Fi networks..." | tee -a $LOG_FILE
if command -v termux-wifi-scaninfo >/dev/null 2>&1; then
    termux-wifi-scaninfo | tee -a $LOG_FILE
else
    echo "[$DATE] termux-wifi-scaninfo not available, skipping Wi-Fi scan." | tee -a $LOG_FILE
fi

# 3. Ping common IoT IP ranges (local network discovery)
echo "[$DATE] Pinging local IoT network..." | tee -a $LOG_FILE
for ip in $(seq 1 254); do
    ping -c 1 -W 1 192.168.1.$ip >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[$DATE] Active device found: 192.168.1.$ip" | tee -a $LOG_FILE
    fi
done

# 4. Check system resources
echo "[$DATE] Checking system resources..." | tee -a $LOG_FILE
free -h | tee -a $LOG_FILE
top -b -n 1 | head -n 15 | tee -a $LOG_FILE

echo "[$DATE] ===== Omega Scan Completed =====" | tee -a $LOG_FILE
