import json
import time

STATE = {}

# ---------------------------
# UPDATE VALUE
# ---------------------------

def update(key, value):
    STATE[key] = {
        "value": value,
        "timestamp": time.time()
    }

# ---------------------------
# MERGE STATES
# ---------------------------

def merge(remote_state):
    for k, v in remote_state.items():
        if k not in STATE or v["timestamp"] > STATE[k]["timestamp"]:
            STATE[k] = v

# ---------------------------
# EXPORT
# ---------------------------

def export():
    return STATE

if __name__ == "__main__":
    update("system", "active")
    print(export())
