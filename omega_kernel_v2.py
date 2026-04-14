import os
import time
import signal
import threading

from core.orchestrator import Orchestrator
from core.swarm import SwarmNetwork

# -----------------------------
# 🧷 SAFE LOCK SYSTEM (TERMUX)
# -----------------------------
LOCK_FILE = os.path.expanduser("~/Omega/.omega_kernel.lock")
os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            print(f"[KERNEL V2] Already running (PID {pid}) → exit")
        except:
            print("[KERNEL V2] Already running → exit")
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
# 🧠 SAFE SHUTDOWN HANDLERS
# -----------------------------
def shutdown(signum, frame):
    print("\n[KERNEL V2] Shutting down...")
    release_lock()
    os._exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


# -----------------------------
# 🚀 OMEGA KERNEL V2
# -----------------------------
class OmegaKernelV2:
    def __init__(self):
        self.orchestrator = Orchestrator()

        # FIX: proper swarm init
        self.swarm = SwarmNetwork()

        # FIX: hard-safe port assignment
        self.port = 5050   # ← FIXED (replaces MemoryBus issue)

    def boot(self):
        print("[KERNEL V2] OMEGA UNIFIED SYSTEM ONLINE")

        # start orchestrator thread
        threading.Thread(
            target=self.orchestrator.boot,
            daemon=True
        ).start()

        # start swarm listener safely
        threading.Thread(
            target=self.swarm.listen,
            daemon=True
        ).start()

        # heartbeat loop
        while True:
            try:
                self.swarm.broadcast({
                    "type": "heartbeat",
                    "status": "alive",
                    "time": time.time()
                })
            except Exception as e:
                print(f"[KERNEL V2 ERROR] swarm broadcast failed: {e}")

            time.sleep(2)


# -----------------------------
# 🚀 ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        exit()

    try:
        OmegaKernelV2().boot()
    finally:
        release_lock()
