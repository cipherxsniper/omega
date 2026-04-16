import time
import random
import json
import os

BUS_FILE = "omega_v19_self_model.json"


# =============================
# SELF MODEL BUS
# =============================
class SelfModelBus:
    def __init__(self):
        self.state = {
            "tick": 0,

            # V18 inherited concepts
            "attention_budget": 3,
            "focus": 0.5,
            "signals": [],
            "selected": [],

            # V19 SELF MODEL
            "self_model": {
                "predicted_focus": 0.5,
                "predicted_budget": 3,
                "error_history": [],
                "confidence": 0.5
            }
        }
        self.load()

    def load(self):
        if os.path.exists(BUS_FILE):
            try:
                with open(BUS_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    def save(self):
        tmp = BUS_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=2)
        os.replace(tmp, BUS_FILE)


# =============================
# MODULES
# =============================
class Module:
    def __init__(self, name):
        self.name = name
        self.bias = random.uniform(0.4, 1.2)

    def emit(self):
        value = random.random() * self.bias

        return {
            "source": self.name,
            "value": value,
            "score": value + random.uniform(-0.1, 0.1)
        }


# =============================
# ATTENTION SELECTION
# =============================
def select_top_k(signals, k):
    return sorted(signals, key=lambda x: x["score"], reverse=True)[:k]


# =============================
# SELF MODEL PREDICTION (V19 CORE)
# =============================
def predict_self(state):
    model = state["self_model"]

    # simple projection based on past error
    avg_error = sum(model["error_history"][-5:] or [0]) / max(len(model["error_history"][-5:]), 1)

    predicted_focus = state["focus"] + (random.uniform(-0.05, 0.05) - avg_error)
    predicted_budget = state["attention_budget"] + (-1 if avg_error > 0.2 else 1 if avg_error < 0.1 else 0)

    model["predicted_focus"] = max(0.0, min(1.0, predicted_focus))
    model["predicted_budget"] = max(1, min(10, predicted_budget))


# =============================
# ERROR COMPUTATION
# =============================
def compute_error(state, actual_focus):
    model = state["self_model"]

    error = abs(model["predicted_focus"] - actual_focus)

    model["error_history"].append(error)
    model["error_history"] = model["error_history"][-50:]

    # update confidence
    model["confidence"] = max(0.1, 1.0 - sum(model["error_history"][-10:]) / 10)


# =============================
# KERNEL V19
# =============================
class OmegaV19:
    def __init__(self):
        self.state = SelfModelBus()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory")
        ]

    def step(self):
        self.state.state["tick"] += 1
        tick = self.state.state["tick"]

        # -------------------------
        # 1. SELF PREDICTION (BEFORE THINKING)
        # -------------------------
        predict_self(self.state.state)

        # apply predicted adjustments
        self.state.state["attention_budget"] = int(self.state.state["self_model"]["predicted_budget"])

        # -------------------------
        # 2. GENERATE SIGNALS
        # -------------------------
        signals = [m.emit() for m in self.modules]

        # -------------------------
        # 3. SELECT ATTENTION
        # -------------------------
        selected = select_top_k(signals, self.state.state["attention_budget"])

        self.state.state["signals"] = signals
        self.state.state["selected"] = selected

        # -------------------------
        # 4. COMPUTE FOCUS
        # -------------------------
        if selected:
            focus = sum(s["score"] for s in selected) / len(selected)
        else:
            focus = 0.0

        self.state.state["focus"] = focus

        # -------------------------
        # 5. ERROR SIGNAL (REAL SELF-LEARNING)
        # -------------------------
        compute_error(self.state.state, focus)

        # -------------------------
        # 6. SAVE
        # -------------------------
        self.state.save()

        print(
            f"[V19] tick {tick} | "
            f"focus={focus:.3f} | "
            f"budget={self.state.state['attention_budget']} | "
            f"confidence={self.state.state['self_model']['confidence']:.3f}"
        )

    def run(self):
        print("[V19] SELF-MODEL COGNITION LOOP ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV19().run()
