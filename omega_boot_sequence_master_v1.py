import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.home() / "Omega"

# ============================
# BOOT LAYERS (CAUSAL ORDER)
# ============================

BOOT_PLAN = [
    # L0 — Identity Layer
    ("L0", "omega_module_identity_registry_v1.py"),
    ("L0", "omega_execution_type_registry_v1.py"),

    # L1 — Memory / Graph
    ("L1", "omega_causal_memory_graph_v7.py"),
    ("L1", "omega_causal_kernel_graph_v2.py"),

    # L2 — Runtime Observation
    ("L2", "omega_runtime_introspection_layer_v1.py"),
    ("L2", "omega_semantic_lifecycle_interpreter_v1.py"),

    # L3 — Health
    ("L3", "omega_causal_health_graph_v1.py"),
    ("L3", "omega_self_aware_system_health_model_v1.py"),

    # L4 — Prediction
    ("L4", "omega_predictive_collapse_engine_v1.py"),
    ("L4", "omega_predictive_graph_evolution_v4_v5_v6.py"),

    # L5 — Truth reconciliation
    ("L5", "omega_cross_layer_truth_reconciler_v1.py"),
    ("L5", "omega_self_aware_causal_identity_v8.py"),

    # L6 — Runtime repair
    ("L6", "omega_causal_runtime_linker_v1.py"),
    ("L6", "omega_causal_repair_engine_v3.py"),

    # L7 — Policy
    ("L7", "omega_autonomous_self_healing_policy_engine_v1.py"),
    ("L7", "omega_autonomous_repair_orchestrator_v1.py"),

    # L8 — Kernel
    ("L8", "omega_self_stabilizing_kernel_v1.py"),
]

# ============================
# EXECUTION TYPE RULES
# ============================

SERVICE_LAYERS = {"L2", "L3", "L7", "L8"}  # long-running
TASK_LAYERS = {"L0", "L1", "L4", "L5", "L6"}  # run once

# ============================
# CORE EXECUTOR
# ============================

def run_script(path):
    full = ROOT / path

    if not full.exists():
        print(f"❌ MISSING: {path}")
        return False

    try:
        print(f"🚀 RUN: {path}")
        subprocess.run([sys.executable, str(full)], check=False)
        return True
    except Exception as e:
        print(f"❌ ERROR: {path} → {e}")
        return False


# ============================
# BOOT ENGINE
# ============================

def boot_system():
    print("\n🧠 OMEGA BOOT SEQUENCE MASTER v1\n")

    boot_state = {
        "success": [],
        "failed": [],
        "skipped": []
    }

    current_layer = None

    for layer, script in BOOT_PLAN:

        if layer != current_layer:
            print(f"\n────────────────────────")
            print(f"🧬 ENTERING LAYER {layer}")
            print(f"────────────────────────")
            current_layer = layer
            time.sleep(0.3)

        ok = run_script(script)

        if ok:
            boot_state["success"].append(script)
        else:
            boot_state["failed"].append(script)

        # stabilization pause between layers
        time.sleep(0.5)

    # ============================
    # SUMMARY
    # ============================

    print("\n🧠 BOOT COMPLETE\n")

    print("✔ SUCCESS:", len(boot_state["success"]))
    print("❌ FAILED:", len(boot_state["failed"]))

    if boot_state["failed"]:
        print("\n⚠️ FAILED MODULES:")
        for f in boot_state["failed"]:
            print(" -", f)

    print("\n🧠 SYSTEM STATUS: INITIALIZATION COMPLETE\n")


# ============================
# ENTRY POINT
# ============================

if __name__ == "__main__":
    boot_system()
