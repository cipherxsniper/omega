#!/bin/bash

while true
do
    python3 observer_v27.py
    echo "⚠️ node crashed → restarting..."
    sleep 1
done
