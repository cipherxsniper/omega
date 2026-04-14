import subprocess
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"
V6_ROOT = OMEGA_ROOT / "OmegaV6"

# =========================
# BOOT LAYERS
# =========================

BOOT_SEQUENCE = [
    # LAYER 0
    OMEGA_ROOT / "omega_self_stabilizing_kernel_v1.py",
    OMEGA_ROOT / "omega_execution_type_registry_v1.py",
    OMEGA_ROOT / "omega_module_identity_registry_v1.py",
    OMEGA_ROOT / "omega_self_aware_system_health_model_v1.py",

    # LAYER 1
    OMEGA_ROOT / "omega_causal_kernel_graph_v2.py",
    OMEGA_ROOT / "omega_causal_memory_graph_v7.py",
    OMEGA_ROOT / "omega_self_aware_causal_identity_v8.py",
    OMEGA_ROOT / "omega_semantic_lifecycle_interpreter_v1.py",

    # LAYER 2
    OMEGA_ROOT / "omega_runtime_introspection_layer_v1.py",
    OMEGA_ROOT / "omega_causal_health_graph_v1.py",
    OMEGA_ROOT / "omega_causal_repair_engine_v3.py",
    OMEGA_ROOT / "omega_predictive_collapse_engine_v1.py",
    OMEGA_ROOT / "omega_cross_layer_truth_reconciler_v1.py",

    # LAYER 3
    OMEGA_ROOT / "omega_causal_runtime_linker_v1.py",
    OMEGA_ROOT / "omega_predictive_graph_evolution_v4_v5_v6.py",

    # LAYER 4
    OMEGA_ROOT / "omega_autonomous_self_healing_policy_engine_v1.py",
    OMEGA_ROOT / "omega_autonomous_repair_orchestrator_v1.py",
]

# =========================
# RUNNER
# =========================

def run_file(path):
    if not path.exists():
        print(f"⚠️ missing: {path}")
        return

    print(f"\n🚀 BOOT: {path.name}")
    try:
        subprocess.Popen(["python", str(path)])
    except Exception as e:
        print(f"❌ failed: {path.name} → {e}")


def boot():
    print("\n🧠 OMEGA BOOT COMPILER v2\n")

    # 1. CORE SYSTEM
    for module in BOOT_SEQUENCE:
        run_file(module)

    # 2. START V6 RUNTIME AFTER CORE
    print("\n🧠 STARTING OMEGA V6 RUNTIME\n")

    v6_main = V6_ROOT / "runtime" / "omega_consensus_runtime_v10.py"

    if v6_main.exists():
        run_file(v6_main)
    else:
        print("⚠️ V6 runtime not found")


if __name__ == "__main__":
    boot()
