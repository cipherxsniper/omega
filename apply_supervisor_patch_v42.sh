#!/bin/bash

FILE=~/Omega/omega_integration_bridge_v4_1_v2.py

echo "[Ω PATCH] Applying Supervisor v4.2 connection patch..."

# 1. Add import if not already present
if ! grep -q "omega_supervisor_v42" "$FILE"; then
    sed -i "1i from omega_supervisor_v42 import supervisor" "$FILE"
    echo "[Ω PATCH] Added supervisor import"
fi

# 2. Replace supervisor_handle with supervisor
sed -i "s/supervisor_handle(event_type, line)/supervisor(event_type, line)/g" "$FILE"

echo "[Ω PATCH] Replaced supervisor_handle → supervisor"

echo "[Ω PATCH] COMPLETE ✔"
