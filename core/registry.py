import json
import time

REG_PATH = "registry/node_registry.json"

def load():
    return json.load(open(REG_PATH))

def save(data):
    json.dump(data, open(REG_PATH, "w"), indent=2)

def register_node(node_id):
    data = load()

    data["nodes"][node_id] = {
        "last_seen": time.time(),
        "status": "active"
    }

    data["total_nodes"] = len(data["nodes"])
    data["active_nodes"] = len(data["nodes"])

    save(data)
