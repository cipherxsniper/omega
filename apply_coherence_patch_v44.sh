#!/data/data/com.termux/files/usr/bin/bash

FILE="$HOME/Omega/omega_interface_registry_v44.py"

echo "[Ω PATCH] Applying coherence model fix..."

# ================================
# 1. Replace compute_coherence
# ================================
sed -i '/def compute_coherence/,/return self.coherence_score/c\
    def compute_coherence(self, predicted_issues):\
        total_imports = sum(len(v) for v in self.imports.values())\
        hard_failures = len(self.orphans)\
        predicted_failures = len(predicted_issues)\
\
        total_risk = hard_failures + (predicted_failures * 0.25)\
\
        if total_imports == 0:\
            self.coherence_score = 1.0\
        else:\
            self.coherence_score = max(\
                0.0,\
                1.0 - (total_risk / (total_imports + 1))\
            )\
\
        return self.coherence_score' "$FILE"

echo "[Ω PATCH] Updated compute_coherence() with predictive drift weighting"

# ================================
# 2. Fix engine call
# ================================
sed -i 's/engine.compute_coherence()/engine.compute_coherence(warnings)/g' "$FILE"

echo "[Ω PATCH] Updated engine call to include warnings"

# ================================
# 3. Done
# ================================
echo "[Ω PATCH] COMPLETE ✔ v4.4 coherence model now predictive-aware"
