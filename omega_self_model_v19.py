import os
import time
import json
import random
import math
from collections import defaultdict, deque

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MODEL_FILE = "omega_self_model_v19.json"
MEMORY_FILE = "omega_self_model_memory_v19.json"

LEARNING_RATE = 0.03
HISTORY_WINDOW = 20


# -----------------------------
# 🧠 SELF-MODEL MATRIX
# -----------------------------
class SelfModelMatrix:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random() * 0.01)

        # each brain has a "self identity vector"
        self.identity = defaultdict(lambda: {
            "explore_bias": random.random(),
            "optimize_bias": random.random(),
            "stability": 1.0
        })

        self.load()

    # -------------------------
    # INTERNAL STATE REPRESENTATION
    # -------------------------
    def self_state(self, brain, history):
        if not history:
            return 0.5

        explore_count = sum(1 for h in history if h["decision"] == "explore")
        optimize_count = len(history) - explore_count

        bias = self.identity[brain]

        state_score = (
            explore_count * bias["explore_bias"]
            + optimize_count * bias["optimize_bias"]
        ) / len(history)

        return state_score

    # -------------------------
    # DECISION MODEL (SELF-REFERENTIAL)
    # -------------------------
    def predict(self, brain, features, history):
        base = self.weights[brain]

        state = self.self_state(brain, history)

        for f in features:
            base += self.weights[str(f)] * 0.1

        # self-awareness feedback loop
        base += state * 0.5

        return base

    # -------------------------
    # TRAIN MODEL
    # -------------------------
    def train(self, brain, features, reward, decision, history):
        error = reward - self.weights[brain]

        self.weights[brain] += LEARNING_RATE * error

        for f in features:
            key = str(f)
            self.weights[key] += LEARNING_RATE * error * 0.01

        # -------------------------
        # UPDATE SELF MODEL
        # -------------------------
        bias = self.identity[brain]

        if decision == "explore":
            bias["explore_bias"] *= 1.01
            bias["optimize_bias"] *= 0.999
        else:
            bias["optimize_bias"] *= 1.01
            bias["explore_bias"] *= 0.999

        # stability adjusts based on reward consistency
        if reward > 0.6:
            bias["stability"] *= 1.002
        else:
            bias["stability"] *= 0.998

        self.identity[brain] = bias

    # -----------------------------
    # SAVE / LOAD
    # -----------------------------
    def save(self):
        data = {
            "weights": dict(self.weights),
            "identity": dict(self.identity)
        }

        with open(MODEL_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                for k, v in data.get("weights", {}).items():
                    self.weights[k] = v

                for k, v in data.get("identity", {}).items():
                    self.identity[k] = v

                print("[V19] Self-model loaded")
            except:
                print("[V19] Fresh self-model initialized")


# -----------------------------
# 🧠 MEMORY SYSTEM
# -----------------------------
class SelfMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: deque(maxlen=HISTORY_WINDOW))

    def store(self, brain, features, reward, decision):
        self.memory[brain].append({
            "t": time.time(),
            "features": features,
            "reward": reward,
            "decision": decision
        })

    def get(self, brain):
        return list(self.memory[brain])

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump({k: list(v) for k, v in self.memory.items()}, f, indent=2)


# -----------------------------
# 🧠 FEATURE ENGINE
# -----------------------------
def generate_features():
    return [
        random.random(),
        random.randint(1, 100),
        math.sin(time.time() % 7)
    ]


# -----------------------------
# 🧠 V19 SELF-MODEL SYSTEM
# -----------------------------
class OmegaSelfModelV19:
    def __init__(self):
        self.model = SelfModelMatrix()
        self.memory = SelfMemory()
        self.step = 0
        self.running = True

    def log(self, msg):
        print(f"[V19] {time.strftime('%H:%M:%S')} {msg}")

    # -------------------------
    # BRAIN CYCLE
    # -------------------------
    def brain_tick(self, brain):
        features = generate_features()

        history = self.memory.get(brain)

        score = self.model.predict(brain, features, history)

        decision = "optimize" if score > 0.55 else "explore"

        reward = random.random()

        self.memory.store(brain, features, reward, decision)

        self.model.train(brain, features, reward, decision, history)

        return brain, decision, reward

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("SELF-MODEL LAYER V19 ONLINE")

        while self.running:
            self.step += 1

            results = []

            for brain in BRAINS:
                results.append(self.brain_tick(brain))

            if self.step % 5 == 0:
                self.model.save()
                self.memory.save()

            opt = sum(1 for r in results if r[1] == "optimize")
            exp = len(results) - opt

            self.log(f"STEP {self.step} | OPT={opt} EXP={exp}")

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSelfModelV19().run()
