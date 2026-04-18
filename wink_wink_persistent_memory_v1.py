import json
import os
import hashlib
from collections import deque

MEM_FILE = "wink_wink_memory_v1.json"

short_term = deque(maxlen=200)

def _hash(x):
    return hashlib.sha256(x.encode()).hexdigest()

def load_memory():
    if not os.path.exists(MEM_FILE):
        return {}
    try:
        return json.load(open(MEM_FILE, "r"))
    except:
        return {}

def save_memory(mem):
    with open(MEM_FILE, "w") as f:
        json.dump(mem, f)

def update_memory(sentence, reward):
    mem = load_memory()
    h = _hash(sentence)

    if h not in mem:
        mem[h] = {
            "text": sentence,
            "count": 1,
            "avg_reward": reward
        }
    else:
        mem[h]["count"] += 1
        mem[h]["avg_reward"] = (
            mem[h]["avg_reward"] * 0.9 + reward * 0.1
        )

    save_memory(mem)
    short_term.append(h)

def novelty(sentence):
    h = _hash(sentence)

    mem = load_memory()

    if h in mem:
        # repeated memory reduces novelty
        return max(0.0, 1.0 - (mem[h]["count"] * 0.2))

    return 1.0

def recall_top_k(k=5):
    mem = load_memory()
    sorted_mem = sorted(
        mem.values(),
        key=lambda x: x["avg_reward"],
        reverse=True
    )
    return sorted_mem[:k]
