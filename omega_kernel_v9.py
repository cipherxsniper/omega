import json
import os
import time
import random

STATE_FILE = "omega_swarm_v9.json"


# -------------------------
# BRAINS
# -------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0

        # temporal memory
        self.recent_rewards = []
        self.predicted_reward = 1.0


# -------------------------
# SWARM MATRIX
# -------------------------
class SwarmMatrix:
    def __init__(self):
        self.global_weight = 1.0

    def update(self, avg_reward, prediction_error):
        lr = 0.05

        # combine reward + prediction error
        signal = (avg_reward - 1.0) + prediction_error

        self.global_weight += lr * signal


# -------------------------
# V9 SYSTEM
# -------------------------
class TemporalSwarmV9:
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

                for b, saved in zip(self.brains, data.get("brains", [])):
                    b.bias = saved.get("bias", 0.0)
                    b.recent_rewards = saved.get("recent_rewards", [])

                print("[V9 MEMORY] Loaded temporal state")

            except:
                print("[V9 MEMORY] reset state")

    # -------------------------
    # SAVE
    # -------------------------
    def save(self):
        data = {
            "tick": self.tick,
            "global_weight": self.matrix.global_weight,
            "brains": [
                {
                    "name": b.name,
                    "bias": b.bias,
                    "recent_rewards": b.recent_rewards[-20:]
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

        noise = random.uniform(-0.03, 0.03)

        reward = base + brain.bias + noise

        return reward

    # -------------------------
    # PREDICTION MODEL (simple EMA)
    # -------------------------
    def predict_next(self, brain):
        if not brain.recent_rewards:
            return 1.0

        alpha = 0.3
        prediction = brain.recent_rewards[-1]

        for r in brain.recent_rewards[-5:]:
            prediction = alpha * r + (1 - alpha) * prediction

        return prediction

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        rewards = []
        prediction_errors = []

        for brain in self.brains:
            reward = self.compute_reward(brain)

            # store history
            brain.recent_rewards.append(reward)
            brain.recent_rewards = brain.recent_rewards[-20:]

            # prediction
            predicted = self.predict_next(brain)
            brain.predicted_reward = predicted

            error = reward - predicted

            # learning update
            brain.bias += 0.02 * error

            rewards.append(reward)
            prediction_errors.append(abs(error))

        avg_reward = sum(rewards) / len(rewards)
        avg_error = sum(prediction_errors) / len(prediction_errors)

        # swarm update
        self.matrix.update(avg_reward, avg_error)

        # cross influence
        for brain in self.brains:
            brain.bias += self.matrix.global_weight * 0.003

        self.save()

        print(
            f"[V9] tick {self.tick} | "
            f"avg_reward={avg_reward:.3f} | "
            f"pred_error={avg_error:.3f} | "
            f"global_w={self.matrix.global_weight:.4f}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V9 SWARM] Temporal Prediction Layer ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        TemporalSwarmV9().run()
    except KeyboardInterrupt:
        print("\n[V9] shutdown clean")
