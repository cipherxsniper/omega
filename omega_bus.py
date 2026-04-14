import json
import os
import time

BUS_FILE = "omega_bus.json"


# =========================
# 🧠 INITIALIZE BUS
# =========================
def _init_bus():
    if not os.path.exists(BUS_FILE):
        bus = {
            "nodes": {},
            "signals": [],
            "last_updated": time.time()
        }
        with open(BUS_FILE, "w") as f:
            json.dump(bus, f, indent=2)


# =========================
# 🧠 READ BUS
# =========================
def read_bus():
    _init_bus()
    with open(BUS_FILE, "r") as f:
        return json.load(f)


# =========================
# 🧠 SAFE WRITE (ATOMIC STYLE)
# =========================
def write_bus(bus):
    tmp_file = BUS_FILE + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(bus, f, indent=2)

    os.replace(tmp_file, BUS_FILE)


# =========================
# 🧠 PUBLISH SIGNAL (NODE → GLOBAL BRAIN)
# =========================
def publish(node, signal):
    bus = read_bus()

    # register node state
    bus["nodes"][node] = {
        "signal": signal,
        "timestamp": time.time()
    }

    # append global signal stream
    bus["signals"].append({
        "node": node,
        "signal": signal,
        "timestamp": time.time()
    })

    # memory safety cap (prevents runaway growth)
    if len(bus["signals"]) > 500:
        bus["signals"] = bus["signals"][-500:]

    write_bus(bus)
