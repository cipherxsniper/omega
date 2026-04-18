import json
from core.learning_engine_v21 import embed, find_similar
from core.swarm_memory_v22 import store_event, load_memory
from core.swarm_intelligence_v23 import (
    compute_influence,
    update_influence,
    get_leader,
    mutate_node,
    get_mutation
)

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

    # -------------------------
    # SWARM INTELLIGENCE LAYER
    # -------------------------
    score = compute_influence(event)
    update_influence(node, score)

    mutation = mutate_node(node, score)
    leader, leader_score = get_leader()

    # -------------------------
    # OUTPUT
    # -------------------------
    print("\n🧠 OMEGA v23 SWARM INTELLIGENCE")
    print(f"Node: {node}")
    print(f"CPU={cpu:.2f} MEM={mem:.2f} LOAD={load:.2f}")

    print(f"📊 Influence Score: {score}")
    print(f"🧬 Mutation Factor: {mutation}")

    print(f"👑 Leader Node: {leader} ({leader_score})")

    print(f"🧬 MEMORY SIZE: {len(memory)}")

    if matches:
        best = matches[0]
        print(f"🔁 SIMILAR EVENTS: {len(matches)}")
        print(f"BEST MATCH: {best[0]:.3f}")
        print(f"SOURCE NODE: {best[1]['event']['node']}")
    else:
        print("🔁 SIMILAR EVENTS: 0")
        print("BEST MATCH: 0")

    # -------------------------
    # EMERGENT BEHAVIOR DETECTION
    # -------------------------
    if leader == node:
        print("👑 THIS NODE IS CURRENT SWARM COORDINATOR")

    if cpu > 0.85 and load > 0.85:
        print("⚡ SWARM ANOMALY DETECTED: HIGH LOAD CLUSTER")

def handle(event):
    update(event)
