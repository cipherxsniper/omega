import subprocess
import time
import os

BASE = os.path.expanduser("~/Omega/OmegaV6")

SERVICES = [
    "runtime_v7/core/v9_9_swarm_bus_v2.py",
    "runtime_v7/core/v10_cognitive_event_memory_graph.py",
    "runtime_v7/core/v11_swarm_reasoning_engine.py",
    "runtime_v7/core/v12_swarm_cognition_layer.py",
    "runtime_v7/core/v13_swarm_self_optimization_engine.py",
    "runtime_v7/core/v14_distributed_swarm_sync.py",
    "runtime_v7/core/v15_crypto_swarm_identity.py",
    "runtime_v7/core/v16_swarm_federation_layer.py",
    "runtime_v7/core/v17_swarm_governance_layer.py",
    "runtime_v7/core/v18_swarm_cognition_layer.py",
    "runtime_v7/core/v19_swarm_prediction_engine.py",
    "runtime_v7/core/v20_swarm_self_optimization_engine.py",
    "runtime_v7/core/v21_swarm_coordination_layer.py",
]

def start():
    print("[OMEGA STARTER] BOOTING SWARM STACK...\n")

    for s in SERVICES:
        full = os.path.join(BASE, s)

        print(f"[STARTING] {s}")

        subprocess.Popen(
            ["python", full],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(0.5)

    print("\n[OMEGA] ALL SYSTEMS LAUNCHED\n")


if __name__ == "__main__":
    start()
    while True:
        time.sleep(10)
