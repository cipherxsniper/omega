import os
import time
import signal
import threading

from core.orchestrator import Orchestrator

# -----------------------------
# 🧷 TERMUX SAFE LOCK SYSTEM
# -----------------------------
LOCK_FILE = os.path.expanduser("~/Omega/.omega_kernel.lock")
os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)

self.port = 5050


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            print(f"[KERNEL V1] Already running (PID {pid}) → exit")
        except:
            print("[KERNEL V1] Already running → exit")
        return False

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    return True


def release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass


# -----------------------------
# 🧠 SAFE SHUTDOWN
# -----------------------------
def shutdown(signum, frame):
    print("\n[KERNEL V1] Shutting down...")
    release_lock()
    os._exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


# -----------------------------
# 🚀 KERNEL CORE
# -----------------------------
class OmegaKernelV1:
    def __init__(self):
        self.orchestrator = Orchestrator()

    def boot(self):
        print("[KERNEL V1] Omega Unified System Online")

        thread = threading.Thread(
            target=self.orchestrator.boot,
            daemon=True
        )
        thread.start()

        while True:
            time.sleep(1)


# -----------------------------
# 🚀 ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        exit()

    try:
        OmegaKernelV1().boot()
    finally:
        release_lock()
