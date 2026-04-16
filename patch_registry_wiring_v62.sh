#!/bin/bash

FILE="$HOME/Omega/omega_unified_kernel_v6.py"

echo "[Ω PATCH] Wiring OmegaRuntimeRegistry v6.2 into ingest()..."

# -----------------------------------
# STEP 1: Add registry tick inside ingest()
# -----------------------------------
if ! grep -q "self.registry.tick" "$FILE"; then
  sed -i '/def ingest(/a\
        self.registry.tick(score, drift)' "$FILE"
fi

echo "[Ω PATCH] Injected registry.tick(score, drift)"

# -----------------------------------
# STEP 2: Ensure structured feed output exists
# -----------------------------------
if ! grep -q "self.registry.feed()" "$FILE"; then
  sed -i '/return /a\
        feed = self.registry.feed()' "$FILE"
fi

echo "[Ω PATCH] Injected registry.feed() output hook"

echo "[Ω PATCH] COMPLETE ✔ v6.2 registry wiring active"
