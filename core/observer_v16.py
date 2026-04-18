from core.event_bus_v14 import subscribe
from core.learning_engine_v16 import update, get_dominant, load

def safe_get(payload, key):
    try:
        return payload.get(key, 0)
    except:
        return 0

def handle(event):
    # 🧠 update learning system
    update(event)

    dominant = get_dominant()
    memory = load()

    node = event.get("node", "unknown")
    payload = event.get("payload", {})

    cpu = safe_get(payload, "cpu")
    mem = safe_get(payload, "memory")
    load_v = safe_get(payload, "load")

    # 🧠 derived intelligence signals
    activity_score = (cpu + mem + load_v) / 3
    stability_hint = 1.0 - abs(load_v - 0.5)
    noise_hint = abs(cpu - mem)

    # 🧠 OBSERVER OUTPUT
    print("\n🧠 OMEGA OBSERVER")
    print(f"Node {node} active → CPU={cpu:.2f} MEM={mem:.2f} LOAD={load_v:.2f}")

    print(f"📊 Activity Score: {activity_score:.3f}")
    print(f"⚖️ Stability Hint: {stability_hint:.3f}")
    print(f"📡 Noise Hint: {noise_hint:.3f}")

    print(f"👑 DOMINANT BRAIN: {dominant}")

    # 🧠 dominance logic feedback
    if dominant == node:
        print("⚡ THIS NODE IS CURRENTLY CONTROLLING SYSTEM WEIGHT")

    # 🧠 system health summary
    node_count = len(memory)

    if node_count < 2:
        system_state = "INITIALISING NETWORK"
    elif node_count < 5:
        system_state = "LEARNING PHASE"
    else:
        system_state = "ADAPTIVE MESH ACTIVE"

    print(f"🌐 SYSTEM STATE: {system_state}")
    print(f"📊 LEARNING MEMORY SIZE: {node_count} nodes tracked")

subscribe(handle)
