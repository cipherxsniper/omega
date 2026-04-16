import time
import random
import json
import os
import traceback
from omega_state import OmegaState


# =========================
# 🧠 SAFE UTILITIES
# =========================
def safe_now():
    return time.time()


def clamp(x, min_v=0.0, max_v=1.0):
    return max(min_v, min(max_v, x))


# =========================
# 🧠 EVENT SCHEMA
# =========================
class Event:
    def __init__(self, tick_id, event_type="tick", payload=None):
        self.tick_id = tick_id
        self.type = event_type
        self.payload = payload or {}
        self.timestamp = safe_now()

    def to_dict(self):
        return {
            "tick": self.tick_id,
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }


# =========================
# 🧠 ATTENTION ENGINE (IMPROVED)
# =========================
class AttentionEngine:
    def __init__(self):
        self.history_bias = {}

    def score(self, event: dict):
        base = 0.5

        # temporal importance
        if event.get("type") == "tick":
            base += 0.2

        # reward signal
        if "ml_reward" in event:
            base += float(event["ml_reward"]) * 0.5

        # error penalty
        if "error" in event:
            base -= 0.4

        # recency bias
        tick = event.get("tick", 1)
        base += min(0.3, tick * 0.001)

        return clamp(base)

    def select(self, events, top_k=3):
        scored = []

        for e in events:
            s = self.score(e)
            scored.append((s, e))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]


# =========================
# 🧠 MODULE SYSTEM (PRODUCTION SAFE)
# =========================
class Module:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn
        self.failures = 0

    def run(self, state, event):
        try:
            result = self.fn(state, event)
            self.failures = 0
            return {
                "module": self.name,
                "output": result,
                "error": None
            }

        except Exception as e:
            self.failures += 1
            return {
                "module": self.name,
                "output": None,
                "error": str(e)
            }


# =========================
# 🧠 OMEGA V28 CORE KERNEL
# =========================
class OmegaKernelV28:
    def __init__(self):
        self.state = OmegaState()
        self.attention = AttentionEngine()

        self.tick_rate = 1
        self.max_memory = 200

        self.modules = self._build_modules()

    # -------------------------
    # MODULE DEFINITIONS
    # -------------------------
    def _build_modules(self):

        def swarm(state, event):
            return {"activity": random.random()}

        def memory(state, event):
            return {"memory_size": len(state.state["memory"])}

        def ml(state, event):
            reward = random.uniform(0.4, 1.2)
            state.state["ml"]["reward"] = reward
            return {"ml_reward": reward}

        def temporal(state, event):
            return {"time": safe_now(), "tick": event.get("tick")}

        def self_model(state, event):
            return {
                "identity": state.get("identity"),
                "stability": state.get("stability")
            }

        return [
            Module("swarm", swarm),
            Module("memory", memory),
            Module("ml", ml),
            Module("temporal", temporal),
            Module("self_model", self_model),
        ]

    # -------------------------
    # MEMORY CONTROL
    # -------------------------
    def _trim_memory(self):
        mem = self.state.state["memory"]
        if len(mem) > self.max_memory:
            self.state.state["memory"] = mem[-self.max_memory:]

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        event = Event(tick).to_dict()

        module_outputs = []

        # run modules
        for m in self.modules:
            out = m.run(self.state, event)
            module_outputs.append(out)

        # ATTENTION SELECTION
        top = self.attention.select(module_outputs, top_k=3)

        # STORE ONLY HIGH VALUE SIGNALS
        for score, signal in top:
            self.state.remember({
                "score": round(score, 4),
                "signal": signal
            })

        # EVENT LOGGING
        self.state.push_event(event)

        # MEMORY CONTROL
        self._trim_memory()

        # SAFE SAVE
        self.state.save()

        # METRICS
        print(
            f"[V28] tick={tick} | "
            f"modules={len(self.modules)} | "
            f"attention={len(top)} | "
            f"memory={len(self.state.state['memory'])}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V28] PRODUCTION COGNITION KERNEL ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


# =========================
# BOOT
# =========================
if __name__ == "__main__":
    OmegaKernelV28().run()
