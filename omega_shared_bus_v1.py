import json
import time
import os

BUS_FILE = "omega_bus_data.json"

def write(node, data):
    state = {}

    if os.path.exists(BUS_FILE):
        with open(BUS_FILE, "r") as f:
            try:
                state = json.load(f)
            except:
                state = {}

    state[node] = {
        "timestamp": time.time(),
        "data": data
    }

    with open(BUS_FILE, "w") as f:
        json.dump(state, f, indent=2)

def read():
    if not os.path.exists(BUS_FILE):
        return {}

    with open(BUS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}
