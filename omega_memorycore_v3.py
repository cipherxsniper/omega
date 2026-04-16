"" OMEGA MEMORYCORE v3 Neural-Structured Memory System Upgrades from v2:

Semantic compression layer

Short-term / long-term memory split

Pattern extraction engine

Anomaly detection on entropy shifts

Lightweight vector-style embeddings (no external deps)

Stable async disk persistence


"""

import json import time import threading import math from collections import deque, defaultdict from datetime import datetime

class OmegaMemoryCoreV3: def init(self, path="omega_memory_v3.json", flush_interval=50, max_short_term=300, max_long_term=2000):

self.path = path
    self.flush_interval = flush_interval

    # short-term raw buffer
    self.short_term = deque(maxlen=max_short_term)

    # long-term compressed memory
    self.long_term = deque(maxlen=max_long_term)

    self.tick_counter = 0
    self.last_flush_tick = 0

    self.lock = threading.Lock()
    self.running = True

    # learned pattern store (simple frequency-based "semantic map")
    self.patterns = defaultdict(int)

    # anomaly tracking
    self.prev_entropy = None
    self.anomalies = []

    # background writer
    self.writer_thread = threading.Thread(target=self._writer_loop, daemon=True)
    self.writer_thread.start()

# -----------------------------
# PUBLIC API
# -----------------------------

def log_state(self, state: dict):
    """Fast ingestion into short-term memory"""

    entropy = state.get("entropy")

    # anomaly detection (entropy shock detection)
    if entropy is not None and self.prev_entropy is not None:
        delta = abs(entropy - self.prev_entropy)
        if delta > 0.15:
            self.anomalies.append({
                "tick": self.tick_counter,
                "delta": delta,
                "state": state
            })

    self.prev_entropy = entropy

    # semantic fingerprint extraction
    signature = self._extract_signature(state)
    self.patterns[signature] += 1

    with self.lock:
        self.short_term.append({
            "tick": self.tick_counter,
            "time": time.time(),
            "state": state,
            "signature": signature
        })

    self.tick_counter += 1

def consolidate(self):
    """Compress short-term memory into long-term representation"""

    with self.lock:
        if not self.short_term:
            return

        batch = list(self.short_term)
        self.short_term.clear()

    # compression: aggregate by signature
    compressed = defaultdict(lambda: {
        "count": 0,
        "avg_entropy": 0,
        "avg_stability": 0,
        "last_seen": None
    })

    for item in batch:
        sig = item["signature"]
        state = item["state"]

        entry = compressed[sig]
        entry["count"] += 1

        entry["avg_entropy"] += state.get("entropy", 0)
        entry["avg_stability"] += state.get("stability", 0)
        entry["last_seen"] = item["time"]

    # finalize averages
    for sig, data in compressed.items():
        data["avg_entropy"] /= data["count"]
        data["avg_stability"] /= data["count"]

        self.long_term.append({
            "signature": sig,
            "data": data
        })

def get_memory_summary(self):
    """Return compressed cognitive snapshot"""
    with self.lock:
        return {
            "ticks": self.tick_counter,
            "short_term_size": len(self.short_term),
            "long_term_size": len(self.long_term),
            "top_patterns": sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:10],
            "anomalies": self.anomalies[-10:]
        }

def save_checkpoint(self):
    """Full structured snapshot"""
    with self.lock:
        snapshot = {
            "created": datetime.utcnow().isoformat(),
            "ticks": self.tick_counter,
            "short_term": list(self.short_term),
            "long_term": list(self.long_term),
            "patterns": dict(self.patterns),
            "anomalies": self.anomalies
        }

    with open(self.path, "w") as f:
        json.dump(snapshot, f)

def stop(self):
    self.running = False
    self.save_checkpoint()

# -----------------------------
# INTERNAL ENGINE
# -----------------------------

def _writer_loop(self):
    while self.running:
        time.sleep(1)

        if self.tick_counter - self.last_flush_tick >= self.flush_interval:
            self.consolidate()
            self.save_checkpoint()
            self.last_flush_tick = self.tick_counter

# -----------------------------
# SEMANTIC LAYER (lightweight)
# -----------------------------

def _extract_signature(self, state: dict):
    """Creates a coarse semantic fingerprint without ML deps"""

    entropy = state.get("entropy", 0)
    stability = state.get("stability", 0)
    nodes = state.get("nodes", 0)

    # discretize into bins
    e_bin = round(entropy * 10)
    s_bin = round(stability * 10)
    n_bin = int(nodes)

    return f"E{e_bin}_S{s_bin}_N{n_bin}"

""" INTEGRATION NOTES:

Replace v2 with:

self.memory = OmegaMemoryCoreV3()

Inside tick: self.memory.log_state(state)

Optional (recommended): self.memory.consolidate()

On shutdown: self.memory.stop() """ ""
