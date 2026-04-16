import json
import os
import time
import random

STATE_FILE = "omega_swarm_v12.json"


# -------------------------
# BRAIN
# -------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0

        # (reward, age, importance)
        self.memory = []


# -------------------------
# SWARM V12
# -------------------------
class TemporalMemorySwarmV12:
    def __init__(self):
        self.brains = [
            Brain("alpha"),
            Brain("beta"),
            Brain("gamma")
        ]

        self.global_weight = 1.0
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
                self.global_weight = data.get("global_weight", 1.0)

                print("[V12] memory loaded")
            except:
                print("[V12] fresh start")

    # -------------------------
    # SAVE
    # -------------------------
    def save(self):
        data = {
            "tick": self.tick,
            "global_weight": self.global_weight
        }

        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)

        os.replace(tmp, STATE_FILE)

    # -------------------------
    # REWARD MODEL
    # -------------------------
    def reward(self, brain):
        noise = random.uniform(-0.05, 0.05)
        return 1.0 + brain.bias + noise

    # -------------------------
    # MEMORY IMPORTANCE
    # -------------------------
    def importance(self, reward, prediction):
        error = abs(reward - prediction)

        # competition signal (same idea as V11 but temporal)
        novelty = random.uniform(0.0, 0.2)

        return error * 0.6 + novelty * 0.4

    # -------------------------
    # MEMORY DECAY FUNCTION
    # -------------------------
    def decay(self, importance, age):
        # HIGH importance = slower decay
        return importance / (1.0 + (age * 0.05))

    # -------------------------
    # PREDICT
    # -------------------------
    def predict(self, brain):
        if not brain.memory:
            return 1.0

        recent = [m[0] for m in brain.memory[-5:]]
        return sum(recent) / len(recent)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        for brain in self.brains:

            r = self.reward(brain)
            p = self.predict(brain)

            imp = self.importance(r, p)

            # STORE MEMORY
            brain.memory.append([r, 0, imp])  # reward, age, importance
            brain.memory = brain.memory[-50:]

            # AGE + DECAY
            new_memory = []

            for reward, age, importance in brain.memory:
                age += 1
                score = self.decay(importance, age)

                # KEEP OR DROP (COMPETITION OVER TIME)
                if score > 0.08:
                    new_memory.append([reward, age, importance])

            brain.memory = new_memory

            # LEARNING FROM SURVIVING MEMORY ONLY
            if brain.memory:
                avg = sum([m[0] for m in brain.memory]) / len(brain.memory)
                brain.bias += 0.02 * (avg - p)

        # GLOBAL SWARM WEIGHT FROM MEMORY SURVIVAL RATE
        total_mem = sum(len(b.memory) for b in self.brains)
        self.global_weight += 0.001 * (total_mem / 10.0 - 1.0)

        self.global_weight = max(0.6, min(1.6, self.global_weight))

        self.save()

        print(
            f"[V12] tick {self.tick} | "
            f"memories={[len(b.memory) for b in self.brains]} | "
            f"global_w={self.global_weight:.4f}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V12 SWARM] Temporal Competitive Memory ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        TemporalMemorySwarmV12().run()
    except KeyboardInterrupt:
        print("\n[V12] shutdown clean")
