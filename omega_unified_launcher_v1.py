import subprocess
import time

print("[Ω-UKS-1] Unified Kernel Starting...")

while True:
    try:
        p = subprocess.Popen(["python", "run_omega_uks1.py"])
        p.wait()
        print("[Ω-UKS-1] Restarting kernel...")

    except Exception as e:
        print("[Ω-UKS-1 ERROR]", e)

    time.sleep(2)
