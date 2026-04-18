#!/bin/bash

FILE="omega_quantum_field_v11.py"

echo "🧠 Applying Omega v12 Clean Execution Patch..."

# 1. Fix imports (remove broken swarm import, fix stability path)
sed -i '/particle_swarm_patch/d' "$FILE"
sed -i 's/from Omega.particle_stability_patch/import stabilize from particle_stability_patch/' "$FILE"
sed -i 's/from Omega.core.omega_cognition_bridge/from core.omega_cognition_bridge/' "$FILE"

# 2. Inject normalize function if missing
if ! grep -q "def normalize_influence" "$FILE"; then
cat << 'PATCH' >> "$FILE"

# =========================
# OMEGA v12 STABILITY PATCH
# =========================
def normalize_influence(inf):
    # handles float, tuple, dict safely
    if isinstance(inf, dict):
        return inf.get("flow_x", 0.0), inf.get("flow_y", 0.0)

    if isinstance(inf, (tuple, list)) and len(inf) >= 2:
        return inf[0], inf[1]

    if isinstance(inf, (int, float)):
        return inf * 0.5, inf * 0.5

    return 0.0, 0.0
PATCH
fi

echo "✅ Patch applied. Run: python3 omega_quantum_field_v11.py"
