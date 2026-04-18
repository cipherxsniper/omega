import time
import json

FILE = "omega_v31_proposals.json"

def propose_edit(agent, target_file, change, reason):
    try:
        data = json.load(open(FILE))
    except:
        data = []

    proposal = {
        "id": len(data) + 1,
        "time": time.time(),
        "agent": agent,
        "target": target_file,
        "change": change,
        "reason": reason,
        "status": "PENDING"
    }

    data.append(proposal)
    json.dump(data, open(FILE, "w"), indent=2)

    return proposal
