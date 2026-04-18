import json, time, os
from collections import deque

BUS_FILE = "omega_global_bus.json"

if not os.path.exists(BUS_FILE):
    with open(BUS_FILE, "w") as f:
        json.dump({"messages": [], "nodes": {}}, f)

def _load():
    with open(BUS_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(BUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def register(node):
    data = _load()
    data["nodes"][node] = {"last_seen": time.time()}
    _save(data)

def publish(node, message, state, signal):
    data = _load()

    data["messages"].append({
        "node": node,
        "message": message,
        "state": state,
        "signal": signal,
        "t": time.time()
    })

    data["messages"] = data["messages"][-200:]  # prevent infinite growth

    _save(data)

def fetch_recent(n=10):
    data = _load()
    return data["messages"][-n:]

def global_signal():
    data = _load()
    msgs = data["messages"]
    if not msgs:
        return 0.5
    return sum(m["signal"] for m in msgs) / len(msgs)
