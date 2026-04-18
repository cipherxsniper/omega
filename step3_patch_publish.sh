#!/bin/bash

echo "🧠 STEP 3 — PATCHING publish() INTO WINK BRAINS"

for f in wink_wink_brain_v*.py; do
    echo "patching $f"

    # add import if missing
    grep -q "omega_mesh_bus_v1" "$f" || sed -i '1i from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal' "$f"

    # register node if missing
    grep -q "NODE_ID" "$f" || sed -i '/while True/i NODE_ID = "'"$f"'"' "$f"

    # replace print() with publish()
    sed -i 's/print(/publish(NODE_ID, /g' "$f"

done

echo "🧠 STEP 3 COMPLETE"
