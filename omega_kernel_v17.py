import json
import time
import os
import random

BUS_FILE = "omega_cognition_bus_v17.json"


# =============================
# COGNITION CORE STATE
# =============================
class CognitionState:
    def __init__(self):
        self.state = {
            "tick": 0,
            "temporal_memory": [],
            "attention_scores": {},
            "self_model": {
                "stability": 1.0,
                "bias": 0.0,
                "performance": []
            },
            "messages": [],
            "global_attention": 1.0
        }
        self.load()

    # -----------------------------
    def load(self):
        if os.path.exists(BUS_FILE):
            try:
                with open(BUS_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    # -----------------------------
    def save(self):
        tmp = BUS_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=2)
        os.replace(tmp, BUS_FILE)

    # -----------------------------
    def add_event(self, event):
        self.state["temporal_memory"].append(event)

        # limit memory growth
        self.state["temporal_memory"] = self.state["temporal_memory"][-100:]


# =============================
# MODULE SIMULATION
# =============================
class Module:
    def __init__(self, name):
        self.name = name

    def emit(self):
        value = random.random()

        return {
            "from": self.name,
            "value": value,
            "time": time.time()
        }


# =============================
# ATTENTION ENGINE (V18 CORE)
# =============================
def compute_attention(events):
    scores = {}

    for e in events:
        src = e["from"]
        val = e["value"]

        score = val * random.uniform(0.8, 1.2)

        if src not in scores:
            scores[src] = 0

        scores[src] += score

    return scores


# =============================
# SELF MODEL (V19 CORE)
# =============================
def update_self_model(state, avg_signal):
    model = state["self_model"]

    # stability drift
    model["stability"] *= 0.999 + (avg_signal * 0.001)

    # bias adaptation
    model["bias"] += (avg_signal - 0.5) * 0.01

    # performance tracking
    model["performance"].append(avg_signal)
    model["performance"] = model["performance"][-50:]


# =============================
# MAIN V17 KERNEL
# =============================
class OmegaV17:
    def __init__(self):
        self.state = CognitionState()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory")
        ]

    def step(self):
        self.state.state["tick"] += 1
        tick = self.state.state["tick"]

        # -------------------------
        # 1. COLLECT EVENTS
        # -------------------------
        events = [m.emit() for m in self.modules]

        for e in events:
            self.state.add_event(e)

        # -------------------------
        # 2. ATTENTION (V18)
        # -------------------------
        attention = compute_attention(events)
        self.state.state["attention_scores"] = attention

        # -------------------------
        # 3. GLOBAL SIGNAL
        # -------------------------
        avg_signal = sum(e["value"] for e in events) / len(events)

        # -------------------------
        # 4. SELF MODEL (V19)
        # -------------------------
        update_self_model(self.state.state, avg_signal)

        # -------------------------
        # 5. SAVE
        # -------------------------
        self.state.save()

        print(
            f"[V17] tick {tick} | "
            f"attention={len(attention)} | "
            f"avg={avg_signal:.3f} | "
            f"stability={self.state.state['self_model']['stability']:.3f}"
        )

    def run(self):
        print("[V17] TEMPORAL + ATTENTION + SELF-MODEL ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV17().run()
