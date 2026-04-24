import json
import time
import os

LOG_DIR = os.path.expanduser("~/Omega/dkf_core_v1/obs/logs")

def log_event(event_type, data):
    os.makedirs(LOG_DIR, exist_ok=True)

    event = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }

    filename = os.path.join(LOG_DIR, "omega_events.jsonl")

    with open(filename, "a") as f:
        f.write(json.dumps(event) + "\n")
