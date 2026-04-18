import json
import time

FILE = "omega_v32_conflicts.json"

def log_conflict(a, b):
    try:
        data = json.load(open(FILE))
    except:
        data = []

    data.append({
        "a": a,
        "b": b,
        "time": time.time()
    })

    json.dump(data, open(FILE, "w"), indent=2)

    return data
