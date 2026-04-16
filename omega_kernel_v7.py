import math

def clamp(x, min_val=-1000, max_val=1000):
    return max(min(x, max_val), min_val)

def squash(x):
    return math.tanh(x)

import json
import os
import time

STATE_FILE = "omega_swarm_memory_v7.json"


class PersistentLearner:
    def __init__(self):
        self.state = {
            "tick": 0,
            "reward_bias": 0.0,
            "history": []
        }
        self.load()

    # -------------------------
    # LOAD MEMORY
    # -------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
                print("[V7 MEMORY] Loaded state")
            except:
                print("[V7 MEMORY] Corrupt state → reset")

    # -------------------------
    # SAVE MEMORY
    # -------------------------
    def save(self):
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f)
        os.replace(tmp, STATE_FILE)

    # -------------------------
    # SIMPLE REWARD FUNCTION
    # -------------------------
    def compute_reward(self, tick):
        """
        This is the FIRST real learning signal.
        Replace later with real environment feedback.
        """

        base = 1.0

        # bias influences reward perception
        adjusted = base + self.state["reward_bias"]

        # mild decay over time
        noise = (tick % 5) * 0.01

        return adjusted - noise

    # -------------------------
    # LEARNING UPDATE
    # -------------------------
    def update_learning(self, reward):
        lr = 0.05

        # move bias toward reward stability
        error = reward - 1.0
        self.state["reward_bias"] += lr * error

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V7] Learning Persistence Engine ONLINE")

        while True:
            self.state["tick"] += 1
            tick = self.state["tick"]

            reward = self.compute_reward(tick)
    # OMEGA_STABILIZED
    reward *= 0.95
    bias *= 0.95
    reward = clamp(reward)
    bias = clamp(bias)
    reward = squash(reward)
    bias = squash(bias)

            self.update_learning(reward)

            event = {
                "tick": tick,
                "reward": reward,
                "bias": self.state["reward_bias"],
                "time": time.time()
            }

            self.state["history"].append(event)
            self.state["history"] = self.state["history"][-200:]

            self.save()

            print(f"[V7] tick {tick} | reward={reward:.3f} | bias={self.state['reward_bias']:.4f}")
    # OMEGA_STABILIZED
    reward *= 0.95
    bias *= 0.95
    reward = clamp(reward)
    bias = clamp(bias)
    reward = squash(reward)
    bias = squash(bias)


            time.sleep(2)


if __name__ == "__main__":
    try:
        PersistentLearner().run()
    except KeyboardInterrupt:
        print("\n[V7] shutdown clean")
