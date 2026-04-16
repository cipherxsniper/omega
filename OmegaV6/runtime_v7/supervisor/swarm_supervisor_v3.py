import subprocess
import time
import json
import os

STATE_FILE = "runtime_v7/supervisor/state.json"

PROCESS_MAP = {
    "bus": {
        "cmd": "python runtime_v7/core/v9_9_swarm_bus_v2.py",
        "log": "logs/bus.log",
        "restarts": 0,
    },
    "v10": {
        "cmd": "python runtime_v7/core/v10_cognitive_event_memory_graph.py",
        "log": "logs/v10.log",
        "restarts": 0,
    },
    "v11": {
        "cmd": "python runtime_v7/core/v11_swarm_reasoning_engine.py",
        "log": "logs/v11.log",
        "restarts": 0,
    },
    "v12": {
        "cmd": "python runtime_v7/core/v12_swarm_cognition_layer.py",
        "log": "logs/v12.log",
        "restarts": 0,
    },
}


# -------------------------
# PERSISTENCE LAYER
# -------------------------
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# -------------------------
# START PROCESS
# -------------------------
def start_process(name, info):
    print(f"[SUPERVISOR] starting {name}")

    log_file = open(info["log"], "a")

    proc = subprocess.Popen(
        info["cmd"].split(),
        stdout=log_file,
        stderr=log_file
    )

    info["proc"] = proc


# -------------------------
# RESTART LOGIC
# -------------------------
def restart_layer(name):
    info = PROCESS_MAP[name]
    info["restarts"] += 1

    print(f"[SUPERVISOR] restarting {name} (count={info['restarts']})")

    start_process(name, info)


# -------------------------
# MONITOR (SELF-HEALING)
# -------------------------
def monitor():
    state = load_state()

    while True:
        for name, info in PROCESS_MAP.items():
            p = info.get("proc")

            if p and p.poll() is not None:
                code = p.returncode

                print("\n" + "=" * 60)
                print(f"[CRASH REPORT] {name}")
                print(f"[EXIT CODE] {code}")
                print("=" * 60 + "\n")

                state[name] = {
                    "last_exit": code,
                    "restarts": info["restarts"],
                    "timestamp": time.time()
                }

                save_state(state)

                # only restart on crash
                if code != 0:
                    time.sleep(3)
                    restart_layer(name)
                else:
                    print(f"[SUPERVISOR] {name} exited cleanly")

        time.sleep(5)


# -------------------------
# BOOTSTRAP
# -------------------------
def main():
    print("[SUPERVISOR V3] BOOTING SELF-HEALING SWARM")

    for name, info in PROCESS_MAP.items():
        start_process(name, info)

    monitor()


if __name__ == "__main__":
    main()
