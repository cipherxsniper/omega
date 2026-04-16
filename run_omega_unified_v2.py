import os
import subprocess
import threading
import time
import signal

OMEGA_ROOT = os.path.dirname(os.path.abspath(__file__))

SYSTEMS = [
    "run_omega_v6.py",
    "run_omega_v9.py",
    "run_omega_kernel_v15.py"
]

processes = []

def stream_output(proc, name):
    for line in iter(proc.stdout.readline, ''):
        if line:
            print(f"[{name}] {line.strip()}")

def start_system(script):
    path = os.path.join(OMEGA_ROOT, script)

    if not os.path.exists(path):
        print(f"[UNIFIED] missing: {script}")
        return None

    print(f"[UNIFIED] launching {script}")

    proc = subprocess.Popen(
        ["python", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    t = threading.Thread(target=stream_output, args=(proc, script), daemon=True)
    t.start()

    return proc

def shutdown(sig=None, frame=None):
    print("\n[UNIFIED] shutting down all omega systems...")
    for p in processes:
        try:
            p.terminate()
        except:
            pass
    exit(0)

signal.signal(signal.SIGINT, shutdown)

def main():
    print("\n======================================")
    print("OMEGA UNIFIED KERNEL v2 (LIVE STREAM)")
    print("======================================\n")

    for s in SYSTEMS:
        p = start_system(s)
        if p:
            processes.append(p)

    while True:
        alive = [p for p in processes if p.poll() is None]

        if not alive:
            print("[UNIFIED] all systems stopped")
            break

        time.sleep(1.5)

if __name__ == "__main__":
    main()

# OPTIMIZED BY v29 ENGINE
