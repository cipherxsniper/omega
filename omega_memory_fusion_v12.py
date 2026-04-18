import json
import time
import os

MEM = os.path.expanduser("~/Omega/omega_memory_v12.json")

def load():
    return json.load(open(MEM))

def record_event(node, event_type, payload):
    db = load()

    db["events"].append({
        "node": node,
        "type": event_type,
        "payload": payload,
        "t": time.time()
    })

    # keep memory bounded
    db["events"] = db["events"][-500:]

    json.dump(db, open(MEM, "w"), indent=2)
