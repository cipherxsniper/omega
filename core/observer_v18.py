from core.event_bus_v14 import subscribe
from core.learning_engine_v18 import update, recall

def handle(event):
    status = update(event)

    match, score = recall(event)

    node = event["node"]
    p = event["payload"]

    print("\n🧠 OMEGA OBSERVER v18")
    print(f"Node: {node}")
    print(f"CPU={p.get('cpu',0):.2f} MEM={p.get('memory',0):.2f} LOAD={p.get('load',0):.2f}")

    if status == "DUPLICATE_SUPPRESSED":
        print("🧯 DUPLICATE EVENT SUPPRESSED")

    if match and score > 0.85:
        print(f"🧠 MEMORY RECALL TRIGGERED (similarity={score:.2f})")
        print(f"📌 Similar past node: {match['event']['node']}")

    print(f"📊 MEMORY ACTIVE EVENTS: updated")

subscribe(handle)
