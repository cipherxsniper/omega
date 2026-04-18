import hashlib
import json
import time

# in-memory lightweight store (swap to Redis later if needed)
MEMORY = []

def embed_event(event: dict):
    """
    Convert event → deterministic lightweight vector (hash-based embedding)
    """
    raw = json.dumps(event, sort_keys=True).encode()
    h = hashlib.sha256(raw).hexdigest()

    # simple vector simulation (NOT ML embedding, but stable signature)
    vector = [int(h[i:i+2], 16) for i in range(0, 32, 2)]

    return {
        "hash": h,
        "vector": vector,
        "timestamp": time.time(),
        "node": event.get("node")
    }


def similarity(v1, v2):
    """cheap similarity = inverse distance"""
    return sum(abs(a - b) for a, b in zip(v1, v2))


def recall(event_embedding, threshold=180):
    """
    Find similar past events
    """
    matches = []

    for m in MEMORY:
        score = similarity(event_embedding["vector"], m["vector"])
        if score < threshold:
            matches.append((score, m))

    return sorted(matches, key=lambda x: x[0])


def store(event):
    emb = embed_event(event)
    MEMORY.append(emb)

    return emb, recall(emb)


def size():
    return len(MEMORY)
