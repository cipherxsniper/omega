import subprocess
import os
import time
import signal
import json

BASE = os.path.dirname(os.path.abspath(__file__))

SYSTEMS = {
    "mesh": "omega_mesh_os_v11.py",
    "bridge": "omega_v20_bridge.py",
    "v20": "omega_recursive_improvement_v20.py",
    "awareness": "omega_self_awareness_v19.py",
    "brain": "quantum_brain.py",
    "unified": "run_omega_unified_v2.py"
}

LOGS = {
    name: f"{name}.log" for name in SYSTEMS
}

PIDS_FILE = "omega_launcher_v3_pids.json"


def start(name, script):
    log_file = open(LOGS[name], "a")

    print(f"[Ω-LAUNCHER v3] Starting {name} -> {script}")

    return subprocess.Popen(
        ["python", os.path.join(BASE, script)],
        stdout=log_file,
        stderr=log_file,
        preexec_fn=os.setsid
    )


def save_pids(pids):
    with open(PIDS_FILE, "w") as f:
        json.dump(pids, f, indent=2)


def main():
    print("\n[Ω-LAUNCHER v3] INITIALIZING SYSTEM CORE\n")

    # SAFER cleanup (only launcher-owned processes)
    if os.path.exists(PIDS_FILE):
        try:
            with open(PIDS_FILE, "r") as f:
                old = json.load(f)

            for pid in old.values():
                try:
                    os.killpg(os.getpgid(pid), signal.SIGTERM)
                    print(f"[Ω-LAUNCHER] Stopped old PID {pid}")
                except:
                    pass
        except:
            pass

    processes = {}

    # ORDERED START (CRITICAL FOR STABILITY)
    start_order = [
        "unified",
        "mesh",
        "bridge",
        "v20",
        "awareness",
        "brain"
    ]

    for name in start_order:
        p = start(name, SYSTEMS[name])
        processes[name] = p.pid
        time.sleep(1.2)

    save_pids(processes)

    print("\n[Ω-LAUNCHER v3] SYSTEM ONLINE")
    print(json.dumps(processes, indent=2))

    # watchdog loop
    try:
        while True:
            time.sleep(5)

            for name, pid in list(processes.items()):
                try:
                    os.kill(pid, 0)
                except:
                    print(f"[Ω-LAUNCHER] WARNING: {name} died — restarting")
                    p = start(name, SYSTEMS[name])
                    processes[name] = p.pid
                    save_pids(processes)

    except KeyboardInterrupt:
        print("\n[Ω-LAUNCHER] SHUTDOWN SIGNAL RECEIVED")

        for pid in processes.values():
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except:
                pass

        print("[Ω-LAUNCHER] CLEAN EXIT")
