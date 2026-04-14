import json
import os
import time
import random

STATE_FILE = "omega_swarm_v8.json"


class SwarmBrain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0
        self.local_reward = 0.0


class SwarmMatrix:
    def __init__(self):
        self.global_weight = 1.0
        self.consensus_strength = 0.1

    def update(self, avg_reward):
        lr = 0.05
        error = avg_reward - 1.0
        self.global_weight += lr * error


class PersistentSwarmV8:
    def __init__(self):
        self.brains = [
            SwarmBrain("alpha"),
            SwarmBrain("beta"),
            SwarmBrain("gamma")
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

                print("[V8 MEMORY] Loaded swarm state")

            except:
                print("[V8 MEMORY] Reset (corrupt state)")

    # -------------------------
    # SAVE STATE
    # -------------------------
    def save(self):
        data = {
            "tick": self.tick,
            "global_weight": self.matrix.global_weight,
            "brains": [
                {"name": b.name, "bias": b.bias}
                for b in self.brains
            ]
        }

        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)

        os.replace(tmp, STATE_FILE)

    # -------------------------
    # REWARD GENERATION
    # -------------------------
    def compute_reward(self, brain):
        base = 1.0

        noise = random.uniform(-0.02, 0.02)

        reward = base + brain.bias + noise

        return reward

    # -------------------------
    # SWARM UPDATE STEP
    # -------------------------
    def step(self):
        self.tick += 1

        rewards = []

        for brain in self.brains:
            reward = self.compute_reward(brain)

            brain.local_reward = reward

            # local learning
            brain.bias += 0.03 * (reward - 1.0)

            rewards.append(reward)

        # global consensus
        avg_reward = sum(rewards) / len(rewards)
        self.matrix.update(avg_reward)

        # cross influence (swarm coupling)
        for brain in self.brains:
            brain.bias += self.matrix.global_weight * 0.005

        self.save()

        print(
            f"[V8] tick {self.tick} | "
            f"avg_reward={avg_reward:.3f} | "
            f"global_w={self.matrix.global_weight:.4f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V8 SWARM] Shared Learning Matrix ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        PersistentSwarmV8().run()
    except KeyboardInterrupt:
        print("\n[V8] shutdown clean")
