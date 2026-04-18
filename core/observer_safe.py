from core.redis_safe import get_redis
from core.scorer import update
from core.registry import register_node
import json

r = get_redis()

CHANNEL = "omega.events"

def to_english(event):
    node = event["node"]
    cpu = event["payload"].get("cpu", 0)
    mem = event["payload"].get("memory", 0)
    load = event["payload"].get("load", 0)

    return (
        f"🧠 OMEGA OBSERVER\n"
        f"Node {node} is ACTIVE\n"
        f"CPU={cpu:.2f} MEM={mem:.2f} LOAD={load:.2f}"
    )

def handle(message):
    try:
        event = json.loads(message["data"])

        register_node(event["node"])
        update(event)

        print(to_english(event), flush=True)
        print("📊 EVENT RECEIVED", flush=True)

    except Exception as e:
        print("⚠️ OBSERVER ERROR:", e, flush=True)

pubsub = r.pubsub()
pubsub.subscribe(CHANNEL)

print("🧠 OBSERVER LISTENING ON omega.events", flush=True)

for message in pubsub.listen():
    if message["type"] == "message":
        handle(message)
