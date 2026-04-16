import time
import random
import json
import os

FILE = "omega_v24_intention.json"


# =============================
# STATE
# =============================
class IntentBus:
    def __init__(self):
        self.state = {
            "tick": 0,

            "goals": [],
            "intents": {},

            "reward_history": [],

            "attention_budget": 3,
            "stability": 1.0
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
            "score": random.random()
        }


# =============================
# ATTENTION
# =============================
def select(signals, k):
    return sorted(signals, key=lambda x: x["score"], reverse=True)[:k]


# =============================
# GOAL UPDATE
# =============================
def update_goals(state, selected):
    for s in selected:
        found = False

        for g in state["goals"]:
            if g["name"] == s["source"]:
                g["count"] += 1
                g["strength"] += 0.05
                found = True

        if not found:
            state["goals"].append({
                "name": s["source"],
                "count": 1,
                "strength": 0.3
            })


# =============================
# INTENTION BUILDER (CORE V24)
# =============================
def build_intentions(state):
    intents = {}

    for g in state["goals"]:
        name = g["name"]

        if name not in intents:
            intents[name] = {
                "strength": 0,
                "count": 0,
                "reward_alignment": 0
            }

        intents[name]["strength"] += g["strength"]
        intents[name]["count"] += g["count"]

    # normalize + temporal smoothing
    for k, v in intents.items():
        v["strength"] = v["strength"] / max(v["count"], 1)

    state["intents"] = intents


# =============================
# INTENTION STABILITY SCORE
# =============================
def compute_intent_stability(state):
    intents = state["intents"]

    if not intents:
        return 1.0

    strengths = [v["strength"] for v in intents.values()]
    avg = sum(strengths) / len(strengths)

    variance = sum((x - avg) ** 2 for x in strengths) / len(strengths)

    stability = max(0.0, 1.0 - variance)

    state["stability"] = 0.9 * state["stability"] + 0.1 * stability


# =============================
# KERNEL V24
# =============================
class OmegaV24:
    def __init__(self):
        self.state = IntentBus()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory"),
            Module("prediction")
        ]

    def step(self):
        self.state.state["tick"] += 1
        tick = self.state.state["tick"]

        # -------------------------
        # 1. SIGNALS
        # -------------------------
        signals = [m.emit() for m in self.modules]

        selected = select(signals, self.state.state["attention_budget"])

        # -------------------------
        # 2. GOALS UPDATE
        # -------------------------
        update_goals(self.state.state, selected)

        # -------------------------
        # 3. BUILD INTENTIONS (🔥 CORE V24)
        # -------------------------
        build_intentions(self.state.state)

        # -------------------------
        # 4. STABILITY
        # -------------------------
        compute_intent_stability(self.state.state)

        # -------------------------
        # 5. REWARD TRACKING
        # -------------------------
        reward = sum(s["score"] for s in selected) / max(len(selected), 1)
        self.state.state["reward_history"].append(reward)

        if len(self.state.state["reward_history"]) > 20:
            self.state.state["reward_history"].pop(0)

        # -------------------------
        # 6. ADAPT ATTENTION VIA INTENTIONS
        # -------------------------
        if self.state.state["intents"]:
            top = max(
                self.state.state["intents"].values(),
                key=lambda x: x["strength"]
            )

            self.state.state["attention_budget"] = max(
                1,
                min(10, int(top["strength"] * 5))
            )

        # -------------------------
        # 7. SAVE
        # -------------------------
        self.state.save()

        # -------------------------
        # 8. OUTPUT
        # -------------------------
        top_intent = None
        if self.state.state["intents"]:
            top_intent = max(
                self.state.state["intents"].items(),
                key=lambda x: x[1]["strength"]
            )[0]

        print(
            f"[V24] tick {tick} | "
            f"goals={len(self.state.state['goals'])} | "
            f"intents={len(self.state.state['intents'])} | "
            f"stability={self.state.state['stability']:.3f} | "
            f"budget={self.state.state['attention_budget']} | "
            f"top_intent={top_intent}"
        )

    def run(self):
        print("[V24] INTENTION FORMATION ENGINE ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV24().run()
