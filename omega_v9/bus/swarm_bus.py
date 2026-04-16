import json
import time
import os

BUS_FILE = "omega_v9_bus.json"

def emit(node, data):
    packet = {
        "node": node,
        "timestamp": time.time(),
        "data": data
    }

    with open(BUS_FILE, "w") as f:
        json.dump(packet, f)

def read():
    if not os.path.exists(BUS_FILE):
        return None

    with open(BUS_FILE) as f:
        return json.load(f)
