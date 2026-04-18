import json
import os
import time

MEM = os.path.expanduser("~/Omega/omega_memory_v13.json")

def load():
    return json.load(open(MEM))

def save(db):
    json.dump(db, open(MEM, "w"), indent=2)

def heal():
    db = load()

    for node, data in db["nodes"].items():
        # decay unstable nodes
        if data["events"] > 50 and data["score"] < 10:
            data["stability"] *= 0.9
            data["score"] *= 0.95

    save(db)
