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
