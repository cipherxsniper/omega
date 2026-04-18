import json
import time

LOG = "omega_v31_audit.json"

def log_event(event):
    try:
        data = json.load(open(LOG))
    except:
        data = []

    data.append({
        "time": time.time(),
        "event": event
    })

    json.dump(data, open(LOG, "w"), indent=2)
