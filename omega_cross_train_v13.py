import json
import os
import time
from omega_embedding_v13 import embed

MEM = os.path.expanduser("~/Omega/omega_memory_v13.json")

def load():
    return json.load(open(MEM))

def save(data):
    json.dump(data, open(MEM, "w"), indent=2)

def train_node(node_id, event_text, reward=1.0):
    db = load()

    if node_id not in db["nodes"]:
        db["nodes"][node_id] = {
            "score": 0,
            "stability": 1.0,
            "events": 0
        }

    # embed event
    vec = embed(event_text)

    db["vectors"].append({
        "node": node_id,
        "embedding": vec,
        "reward": reward
    })

    db["nodes"][node_id]["score"] += reward
    db["nodes"][node_id]["events"] += 1

    db["global_state"]["iteration"] += 1

    save(db)
