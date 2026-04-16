import json
import os
import time
import random

STATE_FILE = "omega_swarm_v11.json"


# -------------------------
# BRAIN ENTITY
# -------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.bias = 0.0
        self.rewards = []
        self.attention_score = 0.0
        self.attention_share = 0.0


# -------------------------
# SWARM CORE
# -------------------------
class CompetitiveSwarmV11:
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
    # LOAD STATE
    # -------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)

                self.tick = data.get("tick", 0)
                self.global_weight = data.get("global_weight", 1.0)

                print("[V11] memory loaded")

            except:
                print("[V11] fresh start")

    # -------------------------
    # SAVE STATE
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
    def compute_reward(self, brain):
        noise = random.uniform(-0.05, 0.05)
        return 1.0 + brain.bias + noise

    # -------------------------
    # ATTENTION SCORING (COMPETITIVE)
    # -------------------------
    def compute_attention_scores(self, rewards, predictions):
        scores = []

        for r, p in zip(rewards, predictions):
            error = abs(r - p)

            # competition signal = error + rarity
            rarity = 1.0 / (1.0 + len([x for x in rewards if abs(x - r) < 0.01]))

            score = error * 0.7 + rarity * 0.3
            scores.append(score)

        return scores

    # -------------------------
    # NORMALIZE ATTENTION (COMPETITION)
    # -------------------------
    def normalize_attention(self, scores):
        total = sum(scores) + 1e-8
        return [s / total for s in scores]

    # -------------------------
    # PREDICT
    # -------------------------
    def predict(self, brain):
        if not brain.rewards:
            return 1.0

        return sum(brain.rewards[-5:]) / min(len(brain.rewards), 5)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        rewards = []
        predictions = []

        # 1. generate signals
        for brain in self.brains:
            r = self.compute_reward(brain)
            p = self.predict(brain)

            brain.rewards.append(r)
            brain.rewards = brain.rewards[-30:]

            rewards.append(r)
            predictions.append(p)

        # 2. compute competition scores
        raw_scores = self.compute_attention_scores(rewards, predictions)
        shares = self.normalize_attention(raw_scores)

        # 3. apply learning with competition
        for brain, r, p, share in zip(self.brains, rewards, predictions, shares):

            brain.attention_score = raw_scores[self.brains.index(brain)]
            brain.attention_share = share

            # COMPETITIVE LEARNING RATE
            lr = 0.01 + (share * 0.08)

            brain.bias += lr * (r - p)

        # 4. swarm coupling (winner-biased)
        winner_idx = shares.index(max(shares))
        winner = self.brains[winner_idx]

        self.global_weight += 0.01 * winner.attention_share
        self.global_weight = max(0.7, min(1.5, self.global_weight))

        self.save()

        print(
            f"[V11] tick {self.tick} | "
            f"winner={winner.name} | "
            f"gw={self.global_weight:.4f} | "
            f"shares={[round(s,3) for s in shares]}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V11 SWARM] Competitive Attention Layer ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    try:
        CompetitiveSwarmV11().run()
    except KeyboardInterrupt:
        print("\n[V11] shutdown clean")
