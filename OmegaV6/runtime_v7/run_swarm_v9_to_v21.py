import os
import subprocess
import time

BASE = "runtime_v7/core"

LAYERS = [
    ("v9_9_swarm_bus_v2.py", "bus"),
    ("v10_cognitive_event_memory_graph.py", "v10"),
    ("v11_swarm_reasoning_engine.py", "v11"),
    ("v12_swarm_cognition_layer.py", "v12"),
    ("v13_swarm_self_optimization_engine.py", "v13"),
    ("v14_distributed_swarm_sync.py", "v14"),
    ("v15_crypto_swarm_identity.py", "v15"),
    ("v16_swarm_federation_layer.py", "v16"),
    ("v17_swarm_governance_layer.py", "v17"),
    ("v18_swarm_cognition_layer.py", "v18"),
    ("v19_swarm_prediction_engine.py", "v19"),
    ("v20_swarm_self_optimization_engine.py", "v20"),
    ("v21_swarm_coordination_layer.py", "v21"),
]

PROCESSES = []


def start_layer(script, name):
    path = os.path.join(BASE, script)
    log_file = f"logs/{name}.log"

    print(f"[LAUNCHER] starting {name} → {script}")

    f = open(log_file, "a")

    p = subprocess.Popen(
        ["python", path],
        stdout=f,
        stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONPATH": os.getcwd()}
    )

    return p


def main():
    print("[SWARM LAUNCHER] BOOTING FULL V9 → V21 STACK")

    for script, name in LAYERS:
        try:
            p = start_layer(script, name)
            PROCESSES.append(p)
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] failed to start {name}: {e}")

    print("\n[SWARM LAUNCHER] ALL SYSTEMS ONLINE\n")

    try:
        while True:
            alive = sum(1 for p in PROCESSES if p.poll() is None)
            print(f"[SWARM STATUS] active_layers={alive}/{len(PROCESSES)}")
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n[SWARM LAUNCHER] SHUTTING DOWN")

        for p in PROCESSES:
            try:
                p.terminate()
            except:
                pass


if __name__ == "__main__":
    main()
