import os
import subprocess
import time
from pathlib import Path

BASE = Path.home() / "Omega"
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)

# ================================
# OMEGA BOOT ORDER (CLEAN + SAFE)
# ================================
BOOT_SEQUENCE = [
    {
        "name": "CORE_SYSTEM",
        "scripts": [
            "omega_execution_type_registry_v1.py",
            "omega_module_identity_registry_v1.py",
            "omega_runtime_introspection_layer_v1.py",
        ],
    },
    {
        "name": "HEALTH_AND_SELF_MODEL",
        "scripts": [
            "omega_self_aware_system_health_model_v1.py",
            "omega_self_aware_causal_identity_v8.py",
            "omega_self_stabilizing_kernel_v1.py",
        ],
    },
    {
        "name": "UNIFIED_BRAIN_LAYER",
        "scripts": [
            "omega_unified_brain_v22.py",
            "omega_meta_brain_v10.py",
            "omega_self_model_v23.py",
        ],
    },
    {
        "name": "MEMORY_AND_MESH",
        "scripts": [
            "omega_memory_federation_v28.py",
            "omega_memory_persistence_v1.py",
            "omega_mesh_bus_v2.py",
            "omega_mesh_orchestrator_v3.py",
        ],
    },
    {
        "name": "COGNITIVE_SYSTEMS",
        "scripts": [
            "omega_cognitive_organism_v4.py",
            "omega_graph_cognition_v3.py",
            "omega_swarm_consciousness_v20.py",
        ],
    },
]

# ================================
# START PROCESS (NOHUP SAFE)
# ================================
def start(script):
    path = BASE / script

    if not path.exists():
        print(f"❌ Missing: {script}")
        return

    log_file = LOGS / f"{script}.log"

    cmd = f"nohup python {path} > {log_file} 2>&1 &"
    os.system(cmd)

    print(f"🚀 Started: {script}")


# ================================
# RUN BOOT SEQUENCE
# ================================
def run_boot():
    print("\n🧠 OMEGA ECOSYSTEM BOOT COMPILER v2\n")

    for stage in BOOT_SEQUENCE:
        print("\n" + "=" * 50)
        print(f"🧩 STAGE: {stage['name']}")
        print("=" * 50)

        for script in stage["scripts"]:
            start(script)
            time.sleep(1)

        print(f"🟢 STAGE COMPLETE: {stage['name']}")
        time.sleep(2)

    print("\n🧠 OMEGA ECOSYSTEM FULLY LAUNCHED")
    print("🤖 Assistant + Brain + Swarm ONLINE")


# ================================
# ENTRY
# ================================
if __name__ == "__main__":
    run_boot()
