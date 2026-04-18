from core.event_bus_v14 import subscribe
from core.swarm_engine_v19 import (
    update_weights,
    get_dominant,
    add_event,
    mutate_score
)

def handle(event):
    node = event["node"]

    payload = event["payload"]
    cpu = payload.get("cpu", 0)
    mem = payload.get("memory", 0)

    # -------------------------
    # 1. SCORE UPDATE (learning)
    # -------------------------
    score_delta = (cpu + mem) / 2
    update_weights(node, score_delta)

    # -------------------------
    # 2. MEMORY DIFFUSION
    # -------------------------
    add_event(event, weight=score_delta)

    # -------------------------
    # 3. MUTATION
    # -------------------------
    mutate_score(node)

    # -------------------------
    # 4. DOMINANT BRAIN
    # -------------------------
    dominant = get_dominant()

    print("\n🧠 OMEGA v19 SWARM OBSERVER")
    print(f"Node: {node}")
    print(f"CPU={cpu:.2f} MEM={mem:.2f}")
    print(f"👑 DOMINANT BRAIN: {dominant}")

    if dominant == node:
        print("⚡ THIS NODE IS CONTROLLING SWARM WEIGHT")

subscribe(handle)
