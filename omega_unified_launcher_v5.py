import os
import subprocess
import time
import json

SYSTEMS = {
    "core":      {"cmd": "run_omega_unified_v2.py", "priority": 0},
    "mesh":      {"cmd": "omega_mesh_os_v11.py", "priority": 1},
    "bridge":    {"cmd": "omega_v20_bridge.py", "priority": 2},
    "v20":       {"cmd": "omega_recursive_improvement_v20.py", "priority": 3},
    "awareness": {"cmd": "omega_self_awareness_v19.py", "priority": 4},
}

STATE_FILE = "omega_global_governance_state.json"

MAX_RESTARTS = 3
RESTART_COOLDOWN = 5

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def kill_all():
    print("[Ω-V5] Killing existing Omega processes...")
    os.system("pkill -f omega")

def start(name, cmd):
    print(f"[Ω-V5] Starting {name} → {cmd}")
    return subprocess.Popen(
        ["python", cmd],
        stdout=open(f"{name}.log", "w"),
        stderr=subprocess.STDOUT
    )

def main():
    kill_all()
    time.sleep(2)

    state = load_state()

    processes = {}

    # sort by priority (GOVERNANCE ORDER)
    ordered = sorted(SYSTEMS.items(), key=lambda x: x[1]["priority"])

    for name, meta in ordered:
        p = start(name, meta["cmd"])
        processes[name] = {
            "pid": p.pid,
            "restarts": 0,
            "cmd": meta["cmd"]
        }
        time.sleep(2)

    print("\n[Ω-V5] GOVERNANCE SYSTEM ONLINE\n")

    while True:
        time.sleep(5)

        for name, info in list(processes.items()):
            pid = info["pid"]

            try:
                os.kill(pid, 0)
            except:
                if info["restarts"] >= MAX_RESTARTS:
                    print(f"[Ω-V5] {name} FAILED governance limit reached → frozen")
                    continue

                print(f"[Ω-V5] {name} crashed → governed restart")

                time.sleep(RESTART_COOLDOWN)

                p = start(name, info["cmd"])

                processes[name]["pid"] = p.pid
                processes[name]["restarts"] += 1

        # write governance snapshot
        save_state({
            "timestamp": time.time(),
            "systems": processes
        })

if __name__ == "__main__":
    main()
