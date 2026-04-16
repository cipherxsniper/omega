#!/data/data/com.termux/files/usr/bin/bash

FILE=~/Omega/omega_unified_kernel_v6.py

echo "[Ω PATCH] Injecting OmegaCoreState into kernel..."

# 1. Ensure import exists (adds if missing)
grep -q "OmegaCoreState" "$FILE" || sed -i "1i from omega_core_state_v61 import OmegaCoreState" "$FILE"

# 2. Inject self.memory initialization into __init__ (safe append after class init line)
sed -i '/def __init__/a\        self.memory = OmegaCoreState()' "$FILE"

echo "[Ω PATCH] COMPLETE ✔ self.memory bound to OmegaCoreState"
