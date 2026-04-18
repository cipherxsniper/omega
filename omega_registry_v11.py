import json
import time
import os

REGISTRY_PATH = os.path.expanduser("~/Omega/omega_registry_v11.json")

def load():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def save(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def register_node(node_id):
    db = load()

    db["nodes"][node_id] = {
        "status": "active",
        "last_seen": time.time(),
        "load": 0.0
    }

    save(db)

def heartbeat(node_id, load=0.0):
    db = load()

    if node_id not in db["nodes"]:
        register_node(node_id)
        db = load()

    db["nodes"][node_id]["last_seen"] = time.time()
    db["nodes"][node_id]["load"] = load

    save(db)

def snapshot():
    return load()
