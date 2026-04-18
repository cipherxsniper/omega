import json
import time
from collections import defaultdict

BUS_FILE = "omega_v29_bus.json"

def load_bus():
    try:
        return json.load(open(BUS_FILE))
    except:
        return {"events": []}

def emit(node, event_type, payload):
    bus = load_bus()

    event = {
        "time": time.time(),
        "node": node,
        "type": event_type,
        "payload": payload
    }

    bus["events"].append(event)

    json.dump(bus, open(BUS_FILE, "w"))

    return event

def recent(bus, limit=5):
    return bus["events"][-limit:]
