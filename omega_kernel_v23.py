import time
import random
import json
import os

FILE = "omega_v23_cognition.json"


# =============================
# COGNITION STATE
# =============================
class CognitionBus:
    def __init__(self):
        self.state = {
            "tick": 0,

            "goals": [],
            "meta_goals": [],

            # V23 cognition rules
            "rules": {
                "attention_gain": 1.0,
                "goal_decay": 0.95,
                "merge_threshold": 0.6,
                "stability_weight": 1.0
            },

            # evolution history
            "rule_history": [],
            "stability_score": 1.0,
            "reward_avg": 1.0
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
# ATTENTION (RULE-BASED)
# =============================
def select(signals, rules, k=3):
    weighted = []

    for s in signals:
        score = s["score"] * rules["attention_gain"]
        weighted.append((score, s))

    weighted.sort(reverse=True, key=lambda x: x[0])

    return [s for _, s in weighted[:k]]


# =============================
# RULE EVALUATION ENGINE
# =============================
def evaluate_rules(state):
    rules = state["rules"]

    # simple feedback loop
    reward = state["reward_avg"]

    # adjust rules based on reward trend
    if reward > 1.05:
        rules["attention_gain"] *= 1.01
        rules["merge_threshold"] *= 0.99

    elif reward < 0.95:
        rules["attention_gain"] *= 0.98
        rules["merge_threshold"] *= 1.02

    # clamp
    rules["attention_gain"] = max(0.5, min(2.0, rules["attention_gain"]))
    rules["merge_threshold"] = max(0.2, min(0.9, rules["merge_threshold"]))


# =============================
# SELF-MODIFICATION PROPOSAL
# =============================
def propose_rule_change(state):
    rules = state["rules"]

    proposal = {
        "tick": state["tick"],
        "before": dict(rules),
        "after": dict(rules),
        "reason": "adaptive tuning"
    }

    # simulate evolution suggestion
    if random.random() > 0.7:
        proposal["after"]["goal_decay"] *= random.uniform(0.98, 1.02)

    return proposal


# =============================
# APPLY SAFE RULE UPDATE
# =============================
def apply_rule(state, proposal):
    state["rules"] = proposal["after"]
    state["rule_history"].append(proposal)


# =============================
# KERNEL V23
# =============================
class OmegaV23:
    def __init__(self):
        self.state = CognitionBus()

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
        # 1. SIGNAL GENERATION
        # -------------------------
        signals = [m.emit() for m in self.modules]

        # -------------------------
        # 2. ATTENTION SELECTION
        # -------------------------
        selected = select(signals, self.state.state["rules"])

        # -------------------------
        # 3. UPDATE REWARD (SIMULATED ENV)
        # -------------------------
        reward = sum(s["score"] for s in selected) / max(len(selected), 1)
        self.state.state["reward_avg"] = reward

        # -------------------------
        # 4. RULE EVALUATION
        # -------------------------
        evaluate_rules(self.state.state)

        # -------------------------
        # 5. SELF-MODIFICATION PROPOSAL
        # -------------------------
        proposal = propose_rule_change(self.state.state)

        # apply cautiously
        if random.random() > 0.5:
            apply_rule(self.state.state, proposal)

        # -------------------------
        # 6. STABILITY TRACKING
        # -------------------------
        self.state.state["stability_score"] = (
            self.state.state["stability_score"] * 0.99 + reward * 0.01
        )

        # -------------------------
        # 7. SAVE STATE
        # -------------------------
        self.state.save()

        # -------------------------
        # 8. OUTPUT
        # -------------------------
        print(
            f"[V23] tick {tick} | "
            f"reward={reward:.3f} | "
            f"stability={self.state.state['stability_score']:.3f} | "
            f"attention_gain={self.state.state['rules']['attention_gain']:.3f} | "
            f"merge_th={self.state.state['rules']['merge_threshold']:.3f}"
        )

    def run(self):
        print("[V23] SELF-MODIFYING COGNITION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV23().run()
