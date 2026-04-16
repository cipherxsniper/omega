import time
import random
import json
import os

FILE = "omega_v21_self_reflection.json"


# =============================
# STATE BUS
# =============================
class ReflectionBus:
    def __init__(self):
        self.state = {
            "tick": 0,
            "attention_budget": 3,
            "focus": 0.5,

            "signals": [],
            "selected": [],

            # V20 goals
            "goals": [],

            # V21 reflection metrics
            "stability_score": 1.0,
            "identity_strength": 0.5
        }
        self.load()

    def load(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    def save(self):
        tmp = FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=2)
        os.replace(tmp, FILE)


# =============================
# MODULE
# =============================
class Module:
    def __init__(self, name):
        self.name = name

    def emit(self):
        return {
            "source": self.name,
            "value": random.random(),
            "score": random.random()
        }


# =============================
# ATTENTION
# =============================
def select_top_k(signals, k):
    return sorted(signals, key=lambda x: x["score"], reverse=True)[:k]


# =============================
# GOAL SCORING (V21 CORE)
# =============================
def score_goal(goal):
    # stability + reinforcement - volatility penalty
    return (
        goal["strength"] +
        (goal["hits"] * 0.05) -
        abs(goal["strength"] - 0.5) * 0.2
    )


# =============================
# GOAL REFLECTION FILTER
# =============================
def reflect_on_goals(state):
    goals = state["goals"]

    if not goals:
        return

    scored = []

    for g in goals:
        g["score"] = score_goal(g)
        scored.append(g)

    # sort by self-evaluation
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)

    # keep only stable goals
    kept = scored[:max(1, len(scored)//2)]

    state["goals"] = kept


# =============================
# SELF ANALYSIS (CORE V21)
# =============================
def compute_self_metrics(state):
    goals = state["goals"]

    if len(goals) < 2:
        state["stability_score"] = 1.0
        state["identity_strength"] = 0.5
        return

    strengths = [g["strength"] for g in goals]

    variance = sum((x - sum(strengths)/len(strengths))**2 for x in strengths) / len(strengths)

    stability = max(0.0, 1.0 - variance)
    identity = sum(strengths) / len(strengths)

    state["stability_score"] = stability
    state["identity_strength"] = identity


# =============================
# KERNEL V21
# =============================
class OmegaV21:
    def __init__(self):
        self.state = ReflectionBus()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory")
        ]

    def step(self):
        self.state.state["tick"] += 1
        tick = self.state.state["tick"]

        # -------------------------
        # 1. SIGNAL GENERATION
        # -------------------------
        signals = [m.emit() for m in self.modules]

        # -------------------------
        # 2. SELECTION
        # -------------------------
        selected = select_top_k(signals, self.state.state["attention_budget"])

        self.state.state["signals"] = signals
        self.state.state["selected"] = selected

        # -------------------------
        # 3. UPDATE GOALS (from V20 assumed state structure)
        # -------------------------
        for s in selected:
            found = False

            for g in self.state.state["goals"]:
                if g["name"] == s["source"]:
                    g["strength"] += 0.05
                    g["hits"] += 1
                    found = True

            if not found:
                self.state.state["goals"].append({
                    "name": s["source"],
                    "strength": 0.3,
                    "hits": 1
                })

        # -------------------------
        # 4. SELF-REFLECTION (🔥 CORE V21)
        # -------------------------
        reflect_on_goals(self.state.state)

        compute_self_metrics(self.state.state)

        # -------------------------
        # 5. ADAPT ATTENTION BASED ON SELF UNDERSTANDING
        # -------------------------
        self.state.state["attention_budget"] = max(
            1,
            min(
                10,
                int(self.state.state["identity_strength"] * 6)
            )
        )

        # -------------------------
        # 6. SAVE STATE
        # -------------------------
        self.state.save()

        # -------------------------
        # 7. OUTPUT
        # -------------------------
        top_goal = None
        if self.state.state["goals"]:
            top_goal = self.state.state["goals"][0]

        print(
            f"[V21] tick {tick} | "
            f"goals={len(self.state.state['goals'])} | "
            f"stability={self.state.state['stability_score']:.3f} | "
            f"identity={self.state.state['identity_strength']:.3f} | "
            f"budget={self.state.state['attention_budget']} | "
            f"top_goal={top_goal['name'] if top_goal else 'none'}"
        )

    def run(self):
        print("[V21] SELF-REFLECTION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV21().run()
