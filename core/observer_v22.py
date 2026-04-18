import json
from core.learning_engine_v21 import embed, similarity, find_similar
from core.swarm_memory_v22 import store_event, load_memory

def update(event):
    vector = embed(event)

    memory = load_memory()
    matches = find_similar(memory, vector)

    store_event(event, vector)

    node = event.get("node")
    payload = event.get("payload", {})

    cpu = payload.get("cpu", 0)
    mem = payload.get("memory", 0)
    load = payload.get("load", 0)

    print("\n🧠 OMEGA OBSERVER v22 (SWARM MEMORY SYNC)")
    print(f"Node: {node}")
    print(f"CPU={cpu:.2f} MEM={mem:.2f} LOAD={load:.2f}")

    print(f"🧬 SWARM MEMORY SIZE: {len(memory)}")

    if matches:
        best = matches[0]
        print(f"🔁 SWARM MATCHES: {len(matches)}")
        print(f"BEST MATCH: {best[0]:.3f}")
        print(f"SOURCE NODE: {best[1]['event']['node']}")
    else:
        print("🔁 SWARM MATCHES: 0")
        print("BEST MATCH: 0")

    # anomaly detection
    if cpu > 0.85 and load > 0.85:
        print("⚡ SWARM ANOMALY: HIGH LOAD CLUSTER")

def handle(event):
    update(event)
