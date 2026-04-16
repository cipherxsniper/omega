import subprocess
import time
import os

def safe_launch(service):
    if not os.path.exists(service):
        print(f"[GUARD] ❌ Missing: {service}")
        return None

    try:
        proc = subprocess.Popen(
            ["python", service],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

        time.sleep(1)

        if proc.poll() is not None:
            err = proc.stderr.read().decode(errors="ignore")
            print(f"[GUARD] ❌ Immediate crash: {service}")
            print(f"[GUARD] → {err[:200]}")
            return None

        print(f"[GUARD] ✅ Running: {service}")
        return proc

    except Exception as e:
        print(f"[GUARD] ❌ Launch error: {service} → {e}")
        return None
