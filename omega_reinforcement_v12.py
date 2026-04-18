import time
import json
import os

MEM = os.path.expanduser("~/Omega/omega_memory_v12.json")

def load():
    return json.load(open(MEM))

def save(data):
    json.dump(data, open(MEM, "w"), indent=2)

def reward(node, value=1.0):
    db = load()

    if node not in db["node_memory"]:
        db["node_memory"][node] = {
            "score": 0,
            "stability": 1.0,
            "events": 0
        }

    db["node_memory"][node]["score"] += value
    db["node_memory"][node]["events"] += 1

    save(db)

def decay():
    db = load()
    for n in db["node_memory"]:
        db["node_memory"][n]["score"] *= 0.99
    save(db)

def dominant_brain():
    db = load()
    if not db["node_memory"]:
        return None

    return max(db["node_memory"].items(), key=lambda x: x[1]["score"])[0]
