#!/bin/bash

echo "🧠 FIXING PUBLISH CONTRACT ACROSS WINK BRAINS"

for f in wink_wink_brain_v*.py; do
    echo "patching $f"

    # replace direct import
    sed -i 's/from omega_mesh_bus_v1 import publish/from wink_bus_safe_wrapper import publish/g' "$f"

done

echo "🧠 CONTRACT FIX COMPLETE"
