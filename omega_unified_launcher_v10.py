import subprocess
import time

while True:
    try:
        print("[LAUNCHER] starting omega kernel...")
        p = subprocess.Popen(["python", "run_omega_v9.py"])
        p.wait()

    except Exception as e:
        print("[LAUNCHER ERROR]", e)

    print("[LAUNCHER] restarting in 2s...")
    time.sleep(2)
