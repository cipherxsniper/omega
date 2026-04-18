# ============================
# 🧬 OMEGA v21 VECTOR MEMORY CORE
# ============================

def embed(event):
    cpu = event["payload"].get("cpu", 0)
    mem = event["payload"].get("memory", 0)
    load = event["payload"].get("load", 0)

    node = hash(event.get("node", "node-default")) % 1000

    return [cpu, mem, load, node / 1000]


def similarity(a, b):
    return sum(x * y for x, y in zip(a, b))


def find_similar(memory, vector, top_k=3, threshold=0.3):
    scored = []

    for item in memory:
        score = similarity(vector, item["vector"])
        if score > threshold:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]
