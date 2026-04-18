import json, math, time, hashlib

MEM_PATH = "memory/omega_memory_v17.json"

def load():
    try:
        with open(MEM_PATH, "r") as f:
            return json.load(f)
    except:
        return {"events": [], "node_weights": {}}

def save(data):
    with open(MEM_PATH, "w") as f:
        json.dump(data, f)

# 🧬 VECTOR ENCODING (lightweight embedding simulation)
def encode(event):
    p = event.get("payload", {})
    cpu = p.get("cpu", 0)
    mem = p.get("memory", 0)
    load = p.get("load", 0)

    entropy = abs(cpu - mem) + abs(load - 0.5)

    return [cpu, mem, load, entropy]

# 📏 EUCLIDEAN SIMILARITY
def distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

# 🧠 DUPLICATE CHECK
def is_duplicate(new_vec, memory, threshold=0.05):
    for e in memory["events"][-50:]:
        if distance(new_vec, e["vector"]) < threshold:
            return True
    return False

# 🧠 STORE EVENT
def store(event):
    data = load()
    vec = encode(event)

    if is_duplicate(vec, data):
        return False  # suppressed duplicate

    data["events"].append({
        "event": event,
        "vector": vec,
        "ts": time.time()
    })

    # keep memory bounded
    data["events"] = data["events"][-500:]

    save(data)
    return True

# 🌐 CROSS NODE WEIGHT UPDATE
def update_node_weight(node, score):
    data = load()
    weights = data.get("node_weights", {})

    weights[node] = weights.get(node, 0) + score
    data["node_weights"] = weights

    save(data)

# 👑 DOMINANT NODE
def get_dominant():
    data = load()
    weights = data.get("node_weights", {})
    if not weights:
        return None

    return max(weights.items(), key=lambda x: x[1])[0]
