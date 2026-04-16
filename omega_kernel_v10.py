import json
import os
import time
import random

STATE_FILE = "omega_swarm_v10.json"


# -------------------------
# BRAIN
# -------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0

        self.recent_rewards = []
        self.attention_memory = []  # (value, attention)

        self.predicted_reward = 1.0


# -------------------------
# SWARM MATRIX
# -------------------------
class SwarmMatrix:
    def __init__(self):
        self.global_weight = 1.0
        self.global_attention = 0.5

    def update(self, avg_reward, avg_attention):
        lr = 0.05

        signal = (avg_reward - 1.0) + (avg_attention - 0.5)

        self.global_weight += lr * signal
        self.global_weight = max(0.1, min(3.0, self.global_weight))


# -------------------------
# V10 SYSTEM
# -------------------------
class AttentionSwarmV10:
    def __init__(self):
        self.brains = [
            Brain("alpha"),
            Brain("beta"),
            Brain("gamma")
        ]

        self.matrix = SwarmMatrix()
        self.tick = 0

        self.load()

    # -------------------------
    # LOAD STATE
    # -------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)

                self.tick = data.get("tick", 0)
                self.matrix.global_weight = data.get("global_weight", 1.0)

                for b, saved in zip(self.brains, data.get("brains", [])):
                    b.bias = saved.get("bias", 0.0)
                    b.attention_memory = saved.get("attention_memory", [])

                print("[V10 MEMORY] Loaded attention state")

            except:
                print("[V10 MEMORY] reset state")

    # -------------------------
    # SAVE STATE
    # -------------------------
    def save(self):
        data = {
            "tick": self.tick,
            "global_weight": self.matrix.global_weight,
            "brains": [
                {
                    "name": b.name,
                    "bias": b.bias,
                    "attention_memory": b.attention_memory[-30:]
                }
                for b in self.brains
            ]
        }

        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)

        os.replace(tmp, STATE_FILE)

    # -------------------------
    # REWARD MODEL
    # -------------------------
    def compute_reward(self, brain):
        base = 1.0
        noise = random.uniform(-0.04, 0.04)
        return base + brain.bias + noise

    # -------------------------
    # ATTENTION MODEL
    # -------------------------
    def compute_attention(self, reward, predicted):
        error = abs(reward - predicted)

        novelty = random.uniform(0, 0.2)

        attention = (error * 0.7) + (novelty * 0.3)

        return max(0.0, min(1.0, attention))

    # -------------------------
    # PREDICTION
    # -------------------------
    def predict(self, brain):
        if not brain.recent_rewards:
            return 1.0

        alpha = 0.25
        p = brain.recent_rewards[-1]

        for r in brain.recent_rewards[-5:]:
            p = alpha * r + (1 - alpha) * p

        return p

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        rewards = []
        attentions = []

        for brain in self.brains:
            reward = self.compute_reward(brain)
            predicted = self.predict(brain)

            attention = self.compute_attention(reward, predicted)

            # store memory with attention
            brain.recent_rewards.append(reward)
            brain.attention_memory.append((reward, attention))

            brain.recent_rewards = brain.recent_rewards[-30:]
            brain.attention_memory = brain.attention_memory[-30:]

            # ATTENTION-WEIGHTED LEARNING
            lr = 0.02 + (attention * 0.05)

            brain.bias += lr * (reward - predicted)

            rewards.append(reward)
            attentions.append(attention)

        avg_reward = sum(rewards) / len(rewards)
        avg_attention = sum(attentions) / len(attentions)

        self.matrix.update(avg_reward, avg_attention)

        # swarm coupling
        for brain in self.brains:
            brain.bias += self.matrix.global_weight * 0.002

        self.save()

        print(
            f"[V10] tick {self.tick} | "
            f"avg_reward={avg_reward:.3f} | "
            f"avg_attention={avg_attention:.3f} | "
            f"global_w={self.matrix.global_weight:.4f}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V10 SWARM] Attention Memory Layer ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        AttentionSwarmV10().run()
    except KeyboardInterrupt:
        print("\n[V10] shutdown clean")
