import json
import os

MEM_PATH = "logs/wink_memory.json"

def load_memory():
    if os.path.exists(MEM_PATH):
        with open(MEM_PATH, "r") as f:
            return json.load(f)
    return {
        "avg_signal": 0.5,
        "instability_history": [],
        "coherence": 0.5
    }

def save_memory(mem):
    os.makedirs("logs", exist_ok=True)
    with open(MEM_PATH, "w") as f:
        json.dump(mem, f)
