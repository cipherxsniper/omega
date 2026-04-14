import time
import random
import json
import os

FILE = "omega_v20_goal_state.json"


# =============================
# GOAL SYSTEM
# =============================
class GoalBus:
    def __init__(self):
        self.state = {
            "tick": 0,
            "attention_budget": 3,
            "focus": 0.5,

            "signals": [],
            "selected": [],

            # 🧠 EMERGENT GOALS
            "goals": []
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
# MODULES
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
# GOAL EXTRACTION (CORE V20)
# =============================
def extract_goals(state):
    goals = state["goals"]

    # track signal sources
    for s in state["selected"]:
        source = s["source"]

        found = False
        for g in goals:
            if g["name"] == source:
                g["strength"] += 0.05
                g["hits"] += 1
                found = True

        if not found:
            goals.append({
                "name": source,
                "strength": 0.3,
                "hits": 1
            })

    # decay weak goals
    new_goals = []
    for g in goals:
        g["strength"] *= 0.97

        if g["strength"] > 0.25:
            new_goals.append(g)

    state["goals"] = new_goals


# =============================
# GOAL PRIORITIZATION
# =============================
def apply_goal_influence(state):
    if not state["goals"]:
        return 1

    top_goal = max(state["goals"], key=lambda x: x["strength"])

    # goal directly influences attention budget
    return max(1, min(10, int(top_goal["strength"] * 5)))


# =============================
# KERNEL V20
# =============================
class OmegaV20:
    def __init__(self):
        self.state = GoalBus()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory")
        ]

    def step(self):
        self.state.state["tick"] += 1
        tick = self.state.state["tick"]

        # -------------------------
        # 1. GENERATE SIGNALS
        # -------------------------
        signals = [m.emit() for m in self.modules]

        # -------------------------
        # 2. ATTENTION SELECTION
        # -------------------------
        selected = select_top_k(signals, self.state.state["attention_budget"])

        self.state.state["signals"] = signals
        self.state.state["selected"] = selected

        # -------------------------
        # 3. GOAL EMERGENCE
        # -------------------------
        extract_goals(self.state.state)

        # -------------------------
        # 4. GOAL DRIVES ATTENTION (IMPORTANT SHIFT)
        # -------------------------
        self.state.state["attention_budget"] = apply_goal_influence(self.state.state)

        # -------------------------
        # 5. GLOBAL FOCUS
        # -------------------------
        if selected:
            self.state.state["focus"] = sum(s["score"] for s in selected) / len(selected)

        # -------------------------
        # 6. SAVE
        # -------------------------
        self.state.save()

        # -------------------------
        # 7. OUTPUT
        # -------------------------
        top_goal = None
        if self.state.state["goals"]:
            top_goal = max(self.state.state["goals"], key=lambda x: x["strength"])

        print(
            f"[V20] tick {tick} | "
            f"goals={len(self.state.state['goals'])} | "
            f"budget={self.state.state['attention_budget']} | "
            f"focus={self.state.state['focus']:.3f} | "
            f"top_goal={top_goal['name'] if top_goal else 'none'}"
        )

    def run(self):
        print("[V20] GOAL EMERGENCE LAYER ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV20().run()
