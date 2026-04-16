import json
import os
import time
import random

STATE_FILE = "omega_swarm_v10_1.json"


# -------------------------
# BRAIN
# -------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0

        self.recent_rewards = []
        self.attention_memory = []


# -------------------------
# SWARM MATRIX (STABLE)
# -------------------------
class SwarmMatrix:
    def __init__(self):
        self.global_weight = 1.0

    def update(self, avg_reward, avg_attention):
        # CENTERED SIGNAL (prevents drift)
        reward_signal = avg_reward - 1.0
        attention_signal = avg_attention - 0.5

        combined = reward_signal + attention_signal

        lr = 0.03
        self.global_weight += lr * combined

        # HARD BOUNDS (CRITICAL FIX)
        self.global_weight = max(0.7, min(1.3, self.global_weight))


# -------------------------
# V10.1 SYSTEM
# -------------------------
class AttentionSwarmV10_1:
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
    # LOAD
    # -------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)

                self.tick = data.get("tick", 0)
                self.matrix.global_weight = data.get("global_weight", 1.0)

                print("[V10.1] memory loaded")

            except:
                print("[V10.1] reset state")

    # -------------------------
    # SAVE
    # -------------------------
    def save(self):
        data = {
            "tick": self.tick,
            "global_weight": self.matrix.global_weight
        }

        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)

        os.replace(tmp, STATE_FILE)

    # -------------------------
    # REWARD (STABLE NORMALIZED)
    # -------------------------
    def compute_reward(self, brain):
        noise = random.uniform(-0.03, 0.03)
        return 1.0 + brain.bias + noise

    # -------------------------
    # PREDICTION
    # -------------------------
    def predict(self, brain):
        if not brain.recent_rewards:
            return 1.0

        # EMA (stable predictor)
        p = brain.recent_rewards[-1]
        alpha = 0.3

        for r in brain.recent_rewards[-5:]:
            p = alpha * r + (1 - alpha) * p

        return p

    # -------------------------
    # ATTENTION (FIXED NORMALIZED VERSION)
    # -------------------------
    def compute_attention(self, reward, predicted):
        error = abs(reward - predicted)

        # stability estimate (prevents collapse)
        stability = 0.02 + error

        # NORMALIZED ATTENTION (KEY FIX)
        attention = error / (error + stability)

        # slight signal diversity
        attention += random.uniform(0, 0.05)

        return max(0.05, min(0.95, attention))

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

            brain.recent_rewards.append(reward)
            brain.recent_rewards = brain.recent_rewards[-30:]

            brain.attention_memory.append((reward, attention))
            brain.attention_memory = brain.attention_memory[-30:]

            # ATTENTION-WEIGHTED LEARNING (STABLE)
            lr = 0.01 + (attention * 0.03)

            brain.bias += lr * (reward - predicted)

            rewards.append(reward)
            attentions.append(attention)

        avg_reward = sum(rewards) / len(rewards)
        avg_attention = sum(attentions) / len(attentions)

        self.matrix.update(avg_reward, avg_attention)

        # bounded swarm coupling (NO DRIFT)
        for brain in self.brains:
            brain.bias += (self.matrix.global_weight - 1.0) * 0.001

        self.save()

        print(
            f"[V10.1] tick {self.tick} | "
            f"avg_reward={avg_reward:.3f} | "
            f"avg_attention={avg_attention:.3f} | "
            f"global_w={self.matrix.global_weight:.4f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V10.1] Stable Attention Swarm ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        AttentionSwarmV10_1().run()
    except KeyboardInterrupt:
        print("\n[V10.1] shutdown clean")
