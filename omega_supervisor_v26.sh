#!/bin/bash

echo "🧠 STARTING OBSERVER_V26 NODE"

while true
do
    python3 observer_v26.py

    echo "⚠️ NODE CRASHED — RESTARTING IN 1s..."
    sleep 1
done
