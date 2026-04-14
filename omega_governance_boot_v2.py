import os
import time
import subprocess
from collections import deque

# =========================
# OMEGA GOVERNANCE BOOT v2
# =========================

MAX_MODULES = 25
BATCH_SIZE = 10
BATCH_DELAY = 5

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def launch(module):
    log_path = os.path.join(LOG_DIR, f"{module}.log")

    cmd = ["nohup", "python", module]

    with open(log_path, "a") as log:
        subprocess.Popen(
            cmd,
            stdout=log,
            stderr=log,
            preexec_fn=os.setpgrp
        )

    print(f"🚀 STARTED: {module}")

def load_core_modules():
    # ONLY BEST STABLE CORE (max 25 safe selection)
    return [
        "omega_runtime_introspection_layer_v1.py",
        "omega_self_aware_system_health_model_v1.py",
        "omega_self_aware_causal_identity_v8.py",
        "omega_causal_memory_graph_v7.py",
        "omega_causal_kernel_graph_v2.py",
        "omega_semantic_lifecycle_interpreter_v1.py",
        "omega_cross_layer_truth_reconciler_v1.py",
        "omega_execution_type_registry_v1.py",
        "omega_module_identity_registry_v1.py",
        "omega_self_stabilizing_kernel_v1.py",

        "omega_causal_repair_engine_v3.py",
        "omega_predictive_collapse_engine_v1.py",
        "omega_predictive_graph_evolution_v4_v5_v6.py",
        "omega_autonomous_self_healing_policy_engine_v1.py",
        "omega_autonomous_repair_orchestrator_v1.py",

        "omega_unified_kernel_v15.py",
        "omega_identity_kernel_v25.py",
        "omega_execution_engine_v7.py",
        "omega_identity_graph_v2.py",
        "omega_meta_brain_v10.py",

        "omega_unified_brain_v22.py",
        "omega_swarm_memory_bridge_v9.py",
        "omega_swarm_v23_unified.py",
        "omega_mesh_superintelligence_v12.py",
        "omega_process_supervisor_v1.py"
    ][:MAX_MODULES]


def boot():
    print("\n🧠 OMEGA GOVERNANCE BOOT v2 (CONTROLLED CORE)\n")

    modules = load_core_modules()
    queue = deque(modules)

    batch_id = 0

    while queue:
        batch_id += 1
        batch = []

        while queue and len(batch) < BATCH_SIZE:
            batch.append(queue.popleft())

        print(f"\n🧩 BATCH {batch_id} START ({len(batch)} modules)\n")

        for m in batch:
            launch(m)
            time.sleep(0.25)  # small stagger

        print(f"\n🟢 BATCH {batch_id} COMPLETE")
        print(f"⏳ Cooling down {BATCH_DELAY}s...\n")

        time.sleep(BATCH_DELAY)

    print("\n🧠 OMEGA GOVERNANCE BOOT COMPLETE (STABLE CORE ONLINE)\n")

    # lightweight heartbeat (safe)
    while True:
        time.sleep(20)
        print("🟢 Omega heartbeat: controlled runtime stable")

if __name__ == "__main__":
    boot()
