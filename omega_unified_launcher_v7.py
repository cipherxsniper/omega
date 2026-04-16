import subprocess
import time
import os

SERVICES = [
    "python run_omega_v6.py",
    "python run_omega_v9.py",
    "python run_omega_kernel_v15.py"
]

def launch_one(cmd):
    print(f"[Ω-V7] launching: {cmd}")
    return subprocess.Popen(cmd, shell=True)

def main():
    print("[Ω-V7] booting governance launcher")

    processes = [launch_one(cmd) for cmd in SERVICES]

    while True:
        for i, p in enumerate(processes):
            if p.poll() is not None:
                print(f"[Ω-V7] restart detected: service {i}")
                processes[i] = launch_one(SERVICES[i])

        time.sleep(3)

if __name__ == "__main__":
    main()
