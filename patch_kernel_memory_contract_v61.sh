#!/bin/bash

FILE="$HOME/Omega/omega_unified_kernel_v6.py"

echo "[Ω PATCH] Enforcing single memory contract (OmegaCoreState v6.1)..."

# 1. Ensure import exists
grep -q "OmegaCoreState" "$FILE" || \
sed -i "1i from omega_core_state_v61 import OmegaCoreState" "$FILE"

# 2. Ensure self.memory exists in __init__
if ! grep -q "self.memory = OmegaCoreState()" "$FILE"; then
  sed -i "/def __init__/a\\
        self.memory = OmegaCoreState()" "$FILE"
fi

echo "[Ω PATCH] Memory contract enforced ✔"
