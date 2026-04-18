import json
import time

LOG = "omega_v30_self_mod_log.json"

def propose_change(node, change_type, description):
    entry = {
        "time": time.time(),
        "node": node,
        "type": change_type,
        "description": description,
        "status": "PENDING_REVIEW"
    }

    try:
        log = json.load(open(LOG))
    except:
        log = []

    log.append(entry)

    json.dump(log, open(LOG, "w"), indent=2)

    return "🧠 Change proposed (not applied): " + description
