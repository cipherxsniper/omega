import json

MEM = "memory/omega_memory_v14.json"

def load():
    return json.load(open(MEM))

def save(data):
    json.dump(data, open(MEM, "w"), indent=2)

def score(event):
    base = 1.0

    payload = event.get("payload", {})

    if payload.get("cpu", 0) > 0.85:
        base -= 0.3

    if event["type"] == "heartbeat":
        base += 0.2

    return base

def update(event):
    data = load()

    node = event["node"]
    s = score(event)

    data["node_scores"][node] = data["node_scores"].get(node, 0) + s

    # learning curve tracking
    data["learning_curve"].append(s)

    save(data)
