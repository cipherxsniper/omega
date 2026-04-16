# ============================================================
# OMEGA UNIFIED KERNEL LAUNCHER v1
# Starts ALL Omega systems in one controlled loop
# ============================================================

import os
import subprocess
import time
import signal

OMEGA_ROOT = os.path.dirname(os.path.abspath(__file__))

SYSTEMS = [
    "run_omega_v6.py",
    "run_omega_v9.py",
    "run_omega_kernel_v15.py"
]

processes = []

def start_system(script):
    path = os.path.join(OMEGA_ROOT, script)

    if not os.path.exists(path):
        print(f"[UNIFIED] missing: {script}")
        return None

    print(f"[UNIFIED] launching {script}")
    return subprocess.Popen(
        ["python", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

def stream_output(proc, name):
    try:
        for line in proc.stdout:
            print(f"[{name}] {line.strip()}")
    except Exception as e:
        print(f"[STREAM ERROR] {name}: {e}")

def shutdown_all(signum=None, frame=None):
    print("\n[UNIFIED] shutting down omega systems...")
    for p in processes:
        try:
            p.terminate()
        except:
            pass
    exit(0)

signal.signal(signal.SIGINT, shutdown_all)

def main():
    print("\n======================================")
    print("OMEGA UNIFIED KERNEL LAUNCHER v1")
    print("======================================\n")

    # launch all systems
    for sys in SYSTEMS:
        proc = start_system(sys)
        if proc:
            processes.append(proc)

    time.sleep(1.5)

    # stream outputs continuously
    while True:
        alive = False

        for i, proc in enumerate(processes):
            if proc.poll() is None:
                alive = True

        if not alive:
            print("[UNIFIED] all systems stopped")
            break

        time.sleep(1)

if __name__ == "__main__":
    main()

# OPTIMIZED BY v29 ENGINE
