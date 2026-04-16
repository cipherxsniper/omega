<<<<<<< HEAD
import time
import json
import threading
import subprocess
import os
from datetime import datetime

# =========================
# 🧠 OMEGA KERNEL STATE
# =========================

KERNEL = {
    "tick": 0,
    "running": True,
    "events": [],
    "modules": {},
    "memory": {},
    "entropy": 0.0,
    "stability": 1.0
}

STATE_FILE = "omega_kernel_state_v2.json"


# =========================
# 🧠 EVENT BUS
# =========================

def emit(event_type, data=None):
    KERNEL["events"].append({
        "type": event_type,
        "data": data,
        "time": str(datetime.now())
    })


def fetch_events():
    events = KERNEL["events"][:]
    KERNEL["events"] = []
    return events


# =========================
# 🧠 MODULE SYSTEM
# =========================

def register_module(name, fn):
    KERNEL["modules"][name] = fn
    emit("module_registered", name)


def run_module(name, payload=None):
    if name in KERNEL["modules"]:
        return KERNEL["modules"][name](payload)
    emit("module_missing", name)


# =========================
# 🧠 BUILT-IN MODULES
# =========================

def module_system(payload):
    return {
        "tick": KERNEL["tick"],
        "entropy": KERNEL["entropy"],
        "stability": KERNEL["stability"]
    }


def module_echo(payload):
    return payload


def module_shell(payload):
    if not payload:
        return "no command"

    return os.popen(payload).read()


# =========================
# 🧠 PHYSICS ENGINE (simple cognition model)
# =========================

def update_physics():
    KERNEL["entropy"] += 0.01
    KERNEL["stability"] = max(0.1, 1.0 - KERNEL["entropy"] * 0.4)


# =========================
# 🧠 KERNEL LOOP
# =========================

def loop():
    while KERNEL["running"]:
        KERNEL["tick"] += 1

        update_physics()

        # system heartbeat event
        emit("tick", {
            "tick": KERNEL["tick"],
            "entropy": KERNEL["entropy"],
            "stability": KERNEL["stability"]
        })

        # persist state
        with open(STATE_FILE, "w") as f:
            json.dump(KERNEL, f, indent=2)

        time.sleep(1)


# =========================
# 🧠 INIT SYSTEM
# =========================

def init():
    register_module("system", module_system)
    register_module("echo", module_echo)
    register_module("shell", module_shell)

    emit("kernel_boot", "Omega OS v2 online")


# =========================
# 🚀 START KERNEL
# =========================

def start():
    init()

    t = threading.Thread(target=loop, daemon=True)
    t.start()

    return t


if __name__ == "__main__":
    print("🧠 OMEGA OS v2 KERNEL STARTING...")
    start()

    while True:
        time.sleep(10)
=======
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
>>>>>>> 71d54e39cdfcdd1862cc6c05708474c3317e4251
