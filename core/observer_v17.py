from core.event_bus_v14 import subscribe
from core.memory_engine_v17 import (
    store,
    get_dominant,
    encode,
    update_node_weight
)

def similarity_score(vec):
    return sum(vec) / len(vec)

def handle(event):
    node = event.get("node", "unknown")

    stored = store(event)

    vec = encode(event)

    score = similarity_score(vec)

    # 🧠 reinforce node based on signal strength
    update_node_weight(node, score if stored else -0.2)

    dominant = get_dominant()

    cpu = event["payload"].get("cpu", 0)
    mem = event["payload"].get("memory", 0)
    load = event["payload"].get("load", 0)

    print("\n🧠 OMEGA v17 OBSERVER")
    print(f"Node: {node}")
    print(f"CPU={cpu:.2f} MEM={mem:.2f} LOAD={load:.2f}")

    print(f"🧬 Vector: {vec}")
    print(f"📊 Stored: {stored}")

    print(f"👑 Dominant Brain: {dominant}")

    if node == dominant:
        print("⚡ ACTIVE CONTROL NODE")

subscribe(handle)
