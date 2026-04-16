import os
import subprocess
import time
import signal

SYSTEMS = [
    ("mesh", "omega_mesh_os_v11.py"),
    ("bridge", "omega_v20_bridge.py"),
    ("v20", "omega_recursive_improvement_v20.py"),
    ("awareness", "omega_self_awareness_v19.py"),
    ("core", "run_omega_unified_v2.py"),
]

PID_FILE = "omega_supervisor_pids.json"

def kill_old():
    print("[Ω-LAUNCHER] Killing old omega processes...")
    os.system("pkill -f omega")

def start(name, script):
    print(f"[Ω-LAUNCHER] Starting {name} -> {script}")
    return subprocess.Popen(
        ["python", script],
        stdout=open(f"{name}.log", "w"),
        stderr=subprocess.STDOUT
    )

def main():
    kill_old()
    time.sleep(1)

    processes = {}

    for name, script in SYSTEMS:
        p = start(name, script)
        processes[name] = p.pid
        time.sleep(2)

    print("\n[Ω-LAUNCHER] ALL SYSTEMS ONLINE\n")
    for k, v in processes.items():
        print(f" - {k}: PID {v}")

    # watchdog loop
    while True:
        time.sleep(5)
        for name, script in SYSTEMS:
            # check if alive
            pid = processes[name]
            try:
                os.kill(pid, 0)
            except:
                print(f"[Ω-WATCHDOG] {name} died → restarting")
                p = start(name, script)
                processes[name] = p.pid

if __name__ == "__main__":
    main()
