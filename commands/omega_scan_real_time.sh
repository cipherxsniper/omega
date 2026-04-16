#!/bin/bash
# omega_scan_real_time.sh
# Continuous real-time Omega IoT + node scanner

LOG_FILE="$HOME/Omega-President/Omega-President/logs/omega_scan.log"
METRICS_LOG="$HOME/Omega-President/Omega-President/logs/omega_metrics_streamer.log"
INTERVAL=10  # seconds between scans

echo "===== Omega Real-Time Scan Started =====" | tee -a $LOG_FILE

while true; do
    DATE=$(date '+%Y-%m-%d %H:%M:%S')

    # --- 1. Node Monitoring ---
    echo "[$DATE] Scanning Omega nodes..." | tee -a $LOG_FILE
    NODE_PROCESSES=$(ps aux | grep -E 'omega_president|check_nodes.py' | grep -v grep)
    if [ -z "$NODE_PROCESSES" ]; then
        echo "[$DATE] No active Omega nodes found." | tee -a $LOG_FILE
    else
        echo "$NODE_PROCESSES" | tee -a $LOG_FILE
    fi

    # --- 2. Wi-Fi Scan ---
    echo "[$DATE] Scanning Wi-Fi networks..." | tee -a $LOG_FILE
    if command -v termux-wifi-scaninfo >/dev/null 2>&1; then
        termux-wifi-scaninfo | tee -a $LOG_FILE
    else
        echo "[$DATE] termux-wifi-scaninfo not available." | tee -a $LOG_FILE
    fi

    # --- 3. Local IoT Device Discovery ---
    SUBNET=$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | cut -d. -f1-3)
    echo "[$DATE] Pinging local IoT subnet $SUBNET.0/24..." | tee -a $LOG_FILE
    for ip in $(seq 1 254); do
        ping -c 1 -W 1 $SUBNET.$ip >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "[$DATE] Active device: $SUBNET.$ip" | tee -a $LOG_FILE
        fi
    done

    # --- 4. System Metrics ---
    echo "[$DATE] System resources snapshot:" | tee -a $LOG_FILE
    free -h | tee -a $LOG_FILE >> $METRICS_LOG
    top -b -n 1 | head -n 15 | tee -a $LOG_FILE >> $METRICS_LOG

    echo "[$DATE] ===== Scan Cycle Complete =====" | tee -a $LOG_FILE
    sleep $INTERVAL
done
