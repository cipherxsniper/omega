import time
import random
import json
import os

BUS_FILE = "omega_v18_attention_bus.json"


# =============================
# MEMORY BUS
# =============================
class AttentionBus:
    def __init__(self):
        self.state = {
            "tick": 0,
            "signals": [],
            "selected": [],
            "attention_budget": 3,   # 🔥 HARD LIMIT = INTELLIGENCE PRESSURE
            "global_focus": 1.0
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
        self.strength = random.uniform(0.5, 1.5)

    def emit(self):
        value = random.random() * self.strength

        return {
            "source": self.name,
            "value": value,
            "noise": random.random() * 0.2,
            "score": 0.0
        }


# =============================
# ATTENTION SCORING (CRITICAL CORE)
# =============================
def score_signals(signals):
    for s in signals:
        # signal quality = value - noise + stability bias
        s["score"] = s["value"] - s["noise"] + random.uniform(-0.05, 0.05)

    return signals


# =============================
# SELECTION ENGINE (V18 CORE)
# =============================
def select_top_k(signals, k):
    sorted_signals = sorted(signals, key=lambda x: x["score"], reverse=True)
    return sorted_signals[:k]


# =============================
# DECAY SYSTEM (FORGOTTEN THOUGHTS)
# =============================
def apply_decay(bus):
    new_signals = []

    for s in bus.state["signals"]:
        s["score"] *= 0.95  # decay

        if s["score"] > 0.2:
            new_signals.append(s)

    bus.state["signals"] = new_signals


# =============================
# KERNEL V18
# =============================
class OmegaV18:
    def __init__(self):
        self.bus = AttentionBus()

        self.modules = [
            Module("ml"),
            Module("swarm"),
            Module("memory")
        ]

    def step(self):
        self.bus.state["tick"] += 1

        # -------------------------
        # 1. GENERATE SIGNALS
        # -------------------------
        new_signals = [m.emit() for m in self.modules]

        # store into global pool
        self.bus.state["signals"].extend(new_signals)

        # -------------------------
        # 2. SCORE ALL SIGNALS
        # -------------------------
        self.bus.state["signals"] = score_signals(self.bus.state["signals"])

        # -------------------------
        # 3. APPLY ATTENTION BUDGET (🔥 CORE INTELLIGENCE STEP)
        # -------------------------
        selected = select_top_k(
            self.bus.state["signals"],
            self.bus.state["attention_budget"]
        )

        self.bus.state["selected"] = selected

        # -------------------------
        # 4. DECAY UNUSED SIGNALS
        # -------------------------
        apply_decay(self.bus)

        # -------------------------
        # 5. ADAPT ATTENTION BUDGET (EMERGENT CONTROL)
        # -------------------------
        avg_score = sum(s["score"] for s in selected) / len(selected)

        if avg_score > 0.7:
            self.bus.state["attention_budget"] = min(10, self.bus.state["attention_budget"] + 1)
        elif avg_score < 0.4:
            self.bus.state["attention_budget"] = max(1, self.bus.state["attention_budget"] - 1)

        # -------------------------
        # 6. GLOBAL FOCUS UPDATE
        # -------------------------
        self.bus.state["global_focus"] = avg_score

        # -------------------------
        # 7. SAVE STATE
        # -------------------------
        self.bus.save()

        # -------------------------
        # 8. OUTPUT
        # -------------------------
        print(
            f"[V18] tick {self.bus.state['tick']} | "
            f"signals={len(self.bus.state['signals'])} | "
            f"selected={len(selected)} | "
            f"budget={self.bus.state['attention_budget']} | "
            f"focus={avg_score:.3f}"
        )

    def run(self):
        print("[V18] ATTENTION ECONOMY ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV18().run()
