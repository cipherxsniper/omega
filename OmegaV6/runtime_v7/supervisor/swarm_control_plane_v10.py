import subprocess
import time
import json
import os
import uuid
from collections import defaultdict, Counter
from threading import Thread

# -----------------------------
# PATHS
# -----------------------------
MEMORY_FILE = "runtime_v7/supervisor/cognitive_memory_graph.json"
COMPRESSED_FILE = "runtime_v7/supervisor/compressed_memory_v10.json"
PATTERN_FILE = "runtime_v7/supervisor/pattern_memory_v10.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# LOAD MEMORY
# =========================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE))
    return {"events": [], "edges": []}


def save_compressed(data):
    json.dump(data, open(COMPRESSED_FILE, "w"), indent=2)


def save_patterns(data):
    json.dump(data, open(PATTERN_FILE, "w"), indent=2)


# =========================================================
# 🧠 V10 INTELLIGENCE CORE
# =========================================================

class MemoryCompressorV10:

    def __init__(self):
        self.patterns = defaultdict(int)

    # -----------------------------
    # SCORE EVENT IMPORTANCE
    # -----------------------------
    def score_event(self, event):
        score = 0.1

        if event.get("type") == "heartbeat":
            score -= 0.05

        if event.get("type") in ["error", "crash"]:
            score += 0.8

        if event.get("type") == "ack":
            score += 0.2

        return max(0.01, score)

    # -----------------------------
    # EXTRACT PATTERNS
    # -----------------------------
    def extract_patterns(self, events):
        sequence_map = []

        for i in range(len(events) - 2):
            seq = (
                events[i].get("type"),
                events[i+1].get("type"),
                events[i+2].get("type")
            )
            self.patterns[seq] += 1
            sequence_map.append(seq)

        return dict(self.patterns)

    # -----------------------------
    # COMPRESS MEMORY
    # -----------------------------
    def compress(self, memory):

        events = memory.get("events", [])

        scored = []
        for e in events:
            e["score"] = self.score_event(e)
            scored.append(e)

        # keep only high value events
        filtered = [e for e in scored if e["score"] > 0.15]

        patterns = self.extract_patterns(filtered)

        compressed = {
            "total_events": len(events),
            "kept_events": len(filtered),
            "compression_ratio": round(len(filtered) / max(1, len(events)), 3),
            "events": filtered[-500:],  # sliding window
            "patterns": patterns
        }

        return compressed


# =========================================================
# LOOP
# =========================================================

def run_loop():
    compressor = MemoryCompressorV10()

    while True:
        mem = load_memory()

        compressed = compressor.compress(mem)

        save_compressed(compressed)
        save_patterns(compressed["patterns"])

        print(
            "[V10 MEMORY] "
            f"raw={len(mem['events'])} "
            f"compressed={compressed['kept_events']} "
            f"patterns={len(compressed['patterns'])}"
        )

        time.sleep(5)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("🧠 V10 MEMORY COMPRESSION LAYER ONLINE")
    run_loop()
