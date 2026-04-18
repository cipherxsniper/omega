import json
import os

MEM = os.path.expanduser("~/Omega/omega_memory_v13.json")

def load():
    return json.load(open(MEM))

def get_dominant():
    db = load()

    nodes = db.get("nodes", {})
    if not nodes:
        return None

    best = max(nodes.items(), key=lambda x: x[1]["score"])

    db["global_state"]["dominant_node"] = best[0]

    json.dump(db, open(MEM, "w"), indent=2)

    return best[0]
