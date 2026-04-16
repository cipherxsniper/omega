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

MODEL_FILE = "omega_goal_model_v20.json"
MEMORY_FILE = "omega_goal_memory_v20.json"

LEARNING_RATE = 0.03
HISTORY_WINDOW = 25
GOAL_THRESHOLD = 3  # pattern repetition needed to form goal


# -----------------------------
# 🧠 GOAL SYSTEM CORE
# -----------------------------
class GoalEngine:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random() * 0.01)

        # emergent goals:
        # goal_name -> {"strength": float, "count": int}
        self.goals = defaultdict(lambda: {"strength": 0.5, "count": 0})

        self.load()

    # -------------------------
    # FEATURE SCORING
    # -------------------------
    def score(self, brain, features):
        score = self.weights[brain]

        for f in features:
            score += self.weights[str(f)] * 0.1

        # apply goal bias
        for g, data in self.goals.items():
            score += data["strength"] * 0.2

        return score

    # -------------------------
    # GOAL EXTRACTION
    # -------------------------
    def extract_goals(self, memory):
        pattern_map = defaultdict(int)

        # detect repeated reward patterns
        for entry in memory:
            if entry["reward"] > 0.6:
                key = str(tuple(entry["features"]))
                pattern_map[key] += 1

        # convert patterns → goals
        for pattern, count in pattern_map.items():
            if count >= GOAL_THRESHOLD:
                self.goals[pattern]["count"] += count
                self.goals[pattern]["strength"] += 0.05 * count

    # -------------------------
    # TRAIN MODEL
    # -------------------------
    def train(self, brain, features, reward):
        error = reward - self.weights[brain]

        self.weights[brain] += LEARNING_RATE * error

        for f in features:
            self.weights[str(f)] += LEARNING_RATE * error * 0.01

    # -------------------------
    # GOAL STABILITY UPDATE
    # -------------------------
    def stabilize_goals(self):
        for g in list(self.goals.keys()):
            self.goals[g]["strength"] *= 0.995

            # prune weak goals
            if self.goals[g]["strength"] < 0.05:
                del self.goals[g]

    # -------------------------
    # SAVE / LOAD
    # -------------------------
    def save(self):
        data = {
            "weights": dict(self.weights),
            "goals": dict(self.goals)
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

                for k, v in data.get("goals", {}).items():
                    self.goals[k] = v

                print("[V20] Goal system loaded")
            except:
                print("[V20] Fresh goal system initialized")


# -----------------------------
# 🧠 MEMORY SYSTEM
# -----------------------------
class GoalMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: deque(maxlen=HISTORY_WINDOW))

    def store(self, brain, features, reward):
        self.memory[brain].append({
            "t": time.time(),
            "features": features,
            "reward": reward
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
        math.sin(time.time() % 10)
    ]


# -----------------------------
# 🧠 V20 GOAL EMERGENCE SYSTEM
# -----------------------------
class OmegaGoalEmergenceV20:
    def __init__(self):
        self.model = GoalEngine()
        self.memory = GoalMemory()
        self.step = 0
        self.running = True

    def log(self, msg):
        print(f"[V20] {time.strftime('%H:%M:%S')} {msg}")

    # -------------------------
    # BRAIN CYCLE
    # -------------------------
    def brain_tick(self, brain):
        features = generate_features()
        reward = random.random()

        self.memory.store(brain, features, reward)

        history = self.memory.get(brain)

        self.model.extract_goals(history)
        self.model.stabilize_goals()

        score = self.model.score(brain, features)

        decision = "optimize" if score > 0.55 else "explore"

        self.model.train(brain, features, reward)

        return brain, decision, reward

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("GOAL EMERGENCE LAYER V20 ONLINE")

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

            self.log(
                f"STEP {self.step} | OPT={opt} EXP={exp} | GOALS={len(self.model.goals)}"
            )

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaGoalEmergenceV20().run()
