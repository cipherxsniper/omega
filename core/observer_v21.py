import json
from core.learning_engine_v21 import embed, similarity
from core.swarm_memory import store, load_all

def find_similar_swarm(memory, vector, top_k=3, threshold=0.3):
    scored = []

    for item in memory:
        score = similarity(vector, item["vector"])
        if score > threshold:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]


def update(event):

    vector = embed(event)

    # ----------------------------
    # SWARM MEMORY LOAD
    # ----------------------------
    memory = load_all()

    matches = find_similar_swarm(memory, vector)

    # ----------------------------
    # STORE INTO REDIS SWARM MEMORY
    # ----------------------------
    store(event, vector)

    # ----------------------------
    # OUTPUT
    # ----------------------------
    node = event.get("node")
    cpu = event["payload"]["cpu"]
    mem = event["payload"]["memory"]
    load = event["payload"]["load"]

    print("\n🧠 OMEGA v21 SWARM OBSERVER")
    print(f"Node: {node}")
    print(f"CPU={cpu:.2f} MEM={mem:.2f} LOAD={load:.2f}")

    print(f"🧬 SWARM MEMORY SIZE: {len(memory)}")

    if matches:
        best = matches[0]
        print(f"🔁 SWARM MATCHES: {len(matches)}")
        print(f"BEST MATCH SCORE: {best[0]:.2f}")
        print(f"SOURCE NODE: {best[1]['event']['node']}")
    else:
        print("🔁 SWARM MATCHES: 0")

    # ----------------------------
    # CROSS-NODE INTELLIGENCE SIGNAL
    # ----------------------------
    if cpu > 0.85 and load > 0.85:
        print("⚡ SWARM ANOMALY DETECTED")

def handle(event):
    update(event)
