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

MODEL_FILE = "omega_attention_model_v18.json"
MEMORY_FILE = "omega_attention_memory_v18.json"

LEARNING_RATE = 0.035
MEMORY_LIMIT = 30


# -----------------------------
# 🧠 SHARED ATTENTION MATRIX
# -----------------------------
class AttentionMatrix:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random() * 0.01)
        self.focus_bias = defaultdict(lambda: 1.0)
        self.load()

    # -------------------------
    # ATTENTION SCORE
    # -------------------------
    def attention(self, brain, features):
        score = self.weights[brain] * self.focus_bias[brain]

        for f in features:
            score += self.weights[str(f)] * 0.2

        return score

    # -------------------------
    # TRAIN ATTENTION
    # -------------------------
    def train(self, brain, features, reward, attention_score):
        error = reward * attention_score - self.weights[brain]

        self.weights[brain] += LEARNING_RATE * error

        # update feature importance
        for f in features:
            key = str(f)
            self.weights[key] += LEARNING_RATE * error * 0.01

        # adjust focus bias dynamically
        if reward > 0.6:
            self.focus_bias[brain] *= 1.01
        else:
            self.focus_bias[brain] *= 0.999

    # -------------------------
    # SAVE / LOAD
    # -------------------------
    def save(self):
        data = {
            "weights": dict(self.weights),
            "focus_bias": dict(self.focus_bias)
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

                for k, v in data.get("focus_bias", {}).items():
                    self.focus_bias[k] = v

                print("[V18] Attention model loaded")
            except:
                print("[V18] Fresh attention model started")


# -----------------------------
# 🧠 ATTENTION MEMORY SYSTEM
# -----------------------------
class AttentionMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: deque(maxlen=MEMORY_LIMIT))

    def store(self, brain, features, reward, attention_score):

        # filter low-attention noise
        if attention_score < 0.2:
            return

        self.memory[brain].append({
            "t": time.time(),
            "features": features,
            "reward": reward,
            "attention": attention_score
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
        math.sin(time.time() % 5)
    ]


# -----------------------------
# 🧠 V18 ATTENTION SWARM
# -----------------------------
class OmegaAttentionV18:
    def __init__(self):
        self.model = AttentionMatrix()
        self.memory = AttentionMemory()
        self.step = 0
        self.running = True

    def log(self, msg):
        print(f"[V18] {time.strftime('%H:%M:%S')} {msg}")

    # -------------------------
    # BRAIN CYCLE
    # -------------------------
    def brain_step(self, brain):
        features = generate_features()
        reward = random.random()

        attention_score = self.model.attention(brain, features)

        decision = "optimize" if attention_score > 0.6 else "explore"

        self.model.train(brain, features, reward, attention_score)
        self.memory.store(brain, features, reward, attention_score)

        return brain, decision, reward, attention_score

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("ATTENTION SWARM V18 ONLINE")

        while self.running:
            self.step += 1

            results = []

            for brain in BRAINS:
                results.append(self.brain_step(brain))

            if self.step % 5 == 0:
                self.model.save()
                self.memory.save()

            opt = sum(1 for r in results if r[1] == "optimize")
            exp = len(results) - opt

            avg_attention = sum(r[3] for r in results) / len(results)

            self.log(
                f"STEP {self.step} | OPT={opt} EXP={exp} | ATT={avg_attention:.3f}"
            )

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaAttentionV18().run()
