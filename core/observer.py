from core.event_bus_v14 import subscribe
from core.scorer import update
from core.registry import register_node
import json

def to_english(event):
    node = event["node"]
    cpu = event["payload"].get("cpu", 0)
    mem = event["payload"].get("memory", 0)

    return f"Node {node} is active. CPU={cpu:.2f}, Memory={mem:.2f}. Event processed."

def handle(event):
    register_node(event["node"])
    update(event)

    with open("registry/node_registry.json") as f:
        reg = json.load(f)

    print("🧠 OMEGA OBSERVER")
    print(to_english(event))
    print(f"📊 NODE COUNT: {reg['total_nodes']}")

subscribe(handle)
