import os
from omega_os_brain_layer_v1 import OmegaOSBrainLayerV1

MODULES = [
    "omega_kernel_v15.py",
    "omega_identity_kernel_v25.py",
    "omega_execution_engine_v7.py",
    "omega_meta_brain_v10.py",
    "omega_swarm_v23_unified.py",
    "omega_process_supervisor_v2.py",
    "omega_os_runtime_v1.py"
]

def boot():
    osb = OmegaOSBrainLayerV1()

    print("\n🧠 OMEGA REAL OS BRAIN CORE v1\n")

    for m in MODULES:
        osb.launch(m, role="core")

    osb.status()

if __name__ == "__main__":
    boot()
