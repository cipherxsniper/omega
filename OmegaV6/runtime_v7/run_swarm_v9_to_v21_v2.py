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

PROCESS_MAP = {}


def start_layer(script, name):
    path = os.path.join(BASE, script)

    log_path = f"logs/{name}.log"
    f = open(log_path, "a")

    print(f"[LAUNCHER] starting {name} → {script}")

    p = subprocess.Popen(
        ["python", path],
        stdout=f,
        stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONPATH": os.getcwd()}
    )

    PROCESS_MAP[name] = {
        "proc": p,
        "script": script,
        "log": log_path,
        "restart_count": 0
    }


def restart_layer(name):
    info = PROCESS_MAP[name]
    script = info["script"]

    print(f"[RESTART] {name} crashed → restarting")

    time.sleep(2)

    start_layer(script, name)
    PROCESS_MAP[name]["restart_count"] += 1


def monitor():
    while True:
        alive = 0

        for name, info in list(PROCESS_MAP.items()):
            p = info["proc"]

            if p.poll() is None:
                alive += 1
            else:
                print(f"[CRASH DETECTED] {name} exited with code {p.returncode}")
                restart_layer(name)

        print(f"[SWARM STATUS] alive={alive}/{len(PROCESS_MAP)}")

        time.sleep(5)


def main():
    print("[SWARM LAUNCHER V2] BOOTING FULL STACK")

    for script, name in LAYERS:
        try:
            start_layer(script, name)
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] {name} failed to start: {e}")

    print("\n[SWARM LAUNCHER V2] ALL SYSTEMS INITIALIZED\n")

    monitor()


if __name__ == "__main__":
    main()
