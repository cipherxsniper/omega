#!/bin/bash

for f in wink_wink_brain_v*.py; do
    echo "patching $f"

    grep -q "omega_mesh_bus_v1" "$f" || sed -i '1i from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal' "$f"

    grep -q "NODE_ID" "$f" || sed -i '/while True/i NODE_ID = "'"$f"'" \nregister(NODE_ID)\n' "$f"

done

echo "ALL BRAINS CONNECTED TO MESH BUS"
