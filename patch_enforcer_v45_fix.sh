#!/data/data/com.termux/files/usr/bin/bash

FILE="$HOME/Omega/omega_coherence_enforcer_v45.py"

echo "[Ω PATCH] Strengthening enforcement gate logic..."

# Replace approval logic block
sed -i '/if score >= COHERENCE_THRESHOLD:/,/return True/c\
    # ================================\
    # STABLE STATE → ONLY IF LOW DRIFT\
    # ================================\
    drift_pressure = len(warnings)\
\
    if score >= COHERENCE_THRESHOLD and drift_pressure < 20:\
        print("[Ω ENFORCER] System stable → EXECUTION APPROVED\n")\
        return True' "$FILE"

# Replace unstable routing condition
sed -i '/# DRIFT DETECTED → ROUTE TO SUPERVISOR/,/print("\n[Ω ENFORCER] EXECUTION BLOCKED UNTIL COHERENCE RESTORED\n")/c\
    # ================================\
    # DRIFT DETECTED → ROUTE TO SUPERVISOR\
    # ================================\
    drift_pressure = len(warnings)\
\
    if drift_pressure >= 20:\
        print("[Ω ENFORCER] HIGH DRIFT → SUPERVISOR REQUIRED\n")' "$FILE"

echo "[Ω PATCH] Enforcer now drift-aware (score + pressure gating)"
