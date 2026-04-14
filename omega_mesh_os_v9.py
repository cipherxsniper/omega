import time
import random
import json
import threading
from collections import defaultdict
import copy


# =========================
# 🧠 CRDT STATE ENGINE
# =========================

class CRDTState:
    """
    Conflict-free replicated state:
    - merge is deterministic
    - no overwrites, only convergence
    """

    def __init__(self):
        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "bias": None,
            "rewards": defaultdict(float),
            "fitness": defaultdict(float),
            "ideas": {},   # global shared idea space
            "history": []
        }

    # -------------------------
    # 🧬 MERGE FUNCTION (CRDT CORE)
    # -------------------------
    def merge(self, incoming):
        for k, v in incoming.items():

            # numeric fields → average merge
            if isinstance(v, (int, float)) and isinstance(self.state.get(k), (int, float)):
                self.state[k] = (self.state[k] + v) / 2

            # dict fields → deep merge
            elif isinstance(v, dict) and isinstance(self.state.get(k), dict):
                self.state[k].update(v)

            # fallback overwrite-safe append
            else:
                self.state[k] = v


# =========================
# 🧠 IDEA ENGINE
# =========================

class IdeaEngine:

    def __init__(self, state):
        self.state = state

    def spawn(self):
        idea_id = f"idea_{random.randint(1000, 9999)}"

        self.state["ideas"][idea_id] = {
            "strength": random.uniform(0.2, 1.0),
            "age": 0,
            "mutation": random.random(),
            "fitness": 0.5
        }

    def evolve(self):
        for k, idea in list(self.state["ideas"].items()):

            # aging
            idea["age"] += 1

            # entropy mutation
            idea["mutation"] += random.uniform(-0.05, 0.05)

            # fitness pressure
            idea["fitness"] = (
                idea["strength"]
                - (idea["age"] * 0.01)
                + (self.state["entropy"] * 0.1)
            )

            # survival pressure
            if idea["fitness"] < 0.2:
                del self.state["ideas"][k]


# =========================
# ⚡ REWARD SYSTEM (v9)
# =========================

class RewardEngine:

    def __init__(self, state):
        self.state = state

    def apply_event(self, event):

        intent = event.get("intent", "none")
        weight = event.get("mesh_weight", 1.0)

        # reward bias system
        self.state["bias"] = intent
        self.state["entropy"] += weight * 0.01

        # assign reward to intent-class idea
        self.state["rewards"][intent] += weight

    def compute_fitness(self):
        for k in self.state["rewards"]:
            reward = self.state["rewards"][k]
            noise = random.uniform(0, 0.05)

            self.state["fitness"][k] = reward - noise


# =========================
# 🌐 MESH KERNEL v9
# =========================

class OmegaMeshV9:

    def __init__(self):
        self.crdt = CRDTState()
        self.ideas = IdeaEngine(self.crdt.state)
        self.reward = RewardEngine(self.crdt.state)

        # bootstrap ideas
        for _ in range(5):
            self.ideas.spawn()

    # -------------------------
    # ⚡ EVENT INGESTION
    # -------------------------
    def ingest_event(self, event):
        self.reward.apply_event(event)

        self.crdt.merge({
            "entropy": self.crdt.state["entropy"],
            "bias": self.crdt.state["bias"],
            "history": [event]
        })

    # -------------------------
    # 🧠 TICK LOOP
    # -------------------------
    def tick(self):
        self.crdt.state["tick"] += 1

        # evolve ideas
        self.ideas.evolve()

        # recompute fitness
        self.reward.compute_fitness()

        # spawn new ideas under entropy pressure
        if self.crdt.state["entropy"] > 0.7:
            self.ideas.spawn()

        # decay entropy slowly
        self.crdt.state["entropy"] *= 0.995

        self.print_state()

    # -------------------------
    # 📡 OUTPUT
    # -------------------------
    def print_state(self):
        print(
            f"[Ω-v9] tick={self.crdt.state['tick']} "
            f"ideas={len(self.crdt.state['ideas'])} "
            f"entropy={round(self.crdt.state['entropy'], 3)} "
            f"bias={self.crdt.state['bias']}"
        )

    # -------------------------
    # 🚀 RUN LOOP
    # -------------------------
    def run(self):
        print("[Ω-MESH v9] CRDT cognitive system ONLINE")

        while True:

            # fake incoming mesh event (replace with your bridge later)
            event = {
                "intent": random.choice(["explore", "mutate", "link", "compress"]),
                "mesh_weight": random.uniform(0.2, 1.5)
            }

            self.ingest_event(event)
            self.tick()

            time.sleep(0.7)


# =========================
# 🚀 BOOT
# =========================

if __name__ == "__main__":
    OmegaMeshV9().run()
