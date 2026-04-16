import json
import time
import random
import threading
from collections import defaultdict, deque
import math

# -----------------------------
# SHARED GLOBAL MEMORY
# -----------------------------
SHARED_MODEL_FILE = "omega_shared_model_v16.json"
SHARED_MEMORY_FILE = "omega_shared_memory.json"


# -----------------------------
# 🧠 SHARED NEURAL MATRIX (v16)
# -----------------------------
class SharedNeuralMatrix:
    def __init__(self):
        self.weights = defaultdict(lambda: random.uniform(-0.5, 0.5))
        self.lr = 0.03
        self.load()

    def predict(self, brain, features):
        score = self.weights[brain]

        for f in features:
            score += self.weights[str(f)] * 0.01

        return score

    def train(self, brain, features, reward):
        error = reward - self.weights[brain]
        self.weights[brain] += self.lr * error

        for f in features:
            self.weights[str(f)] += self.lr * error * 0.01

    def save(self):
        with open(SHARED_MODEL_FILE, "w") as f:
            json.dump(dict(self.weights), f)

    def load(self):
        try:
            with open(SHARED_MODEL_FILE, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    self.weights[k] = v
        except:
            pass


# -----------------------------
# 🧭 TEMPORAL PREDICTION (v17)
# -----------------------------
class TemporalPredictor:
    def __init__(self):
        self.history = deque(maxlen=20)

    def update(self, value):
        self.history.append(value)

    def predict_next(self):
        if len(self.history) < 3:
            return random.random()

        diffs = [
            self.history[i] - self.history[i - 1]
            for i in range(1, len(self.history))
        ]

        return self.history[-1] + sum(diffs[-3:]) / len(diffs[-3:])


# -----------------------------
# 🎯 ATTENTION MEMORY (v18)
# -----------------------------
class AttentionMemory:
    def __init__(self):
        self.memory = []

    def add(self, item):
        score = len(str(item)) * random.uniform(0.8, 1.2)
        self.memory.append((score, item))

    def get_focus(self):
        self.memory.sort(reverse=True)
        return [m[1] for m in self.memory[:5]]


# -----------------------------
# 🧬 SELF MODEL (v19)
# -----------------------------
class SelfModel:
    def __init__(self):
        self.performance = defaultdict(float)

    def update(self, brain, reward):
        self.performance[brain] += reward

    def confidence(self, brain):
        return math.tanh(self.performance[brain])


# -----------------------------
# 🎯 GOAL EMERGENCE (v20)
# -----------------------------
class GoalEmergence:
    def __init__(self):
        self.goals = defaultdict(float)

    def update(self, brain, reward):
        self.goals[brain] += reward * 0.1

    def best_goal(self):
        if not self.goals:
            return "explore"
        return max(self.goals, key=self.goals.get)


# -----------------------------
# 🪞 SELF REFLECTION (v21)
# -----------------------------
class SelfReflection:
    def reflect(self, model, brain):
        conf = model.confidence(brain)

        if conf < 0.3:
            return "unstable"
        elif conf < 0.7:
            return "learning"
        return "stable"


# -----------------------------
# 🧠 GOAL REFINEMENT (v22)
# -----------------------------
class GoalRefinement:
    def refine(self, goals, reflection_state):
        if reflection_state == "unstable":
            return "explore"
        if reflection_state == "learning":
            return "balance"
        return goals.best_goal()


# -----------------------------
# 🧠 UNIFIED BRAIN SYSTEM
# -----------------------------
class OmegaUnifiedBrainV22:
    def __init__(self):
        self.model = SharedNeuralMatrix()
        self.temporal = TemporalPredictor()
        self.attention = AttentionMemory()
        self.self_model = SelfModel()
        self.goals = GoalEmergence()
        self.reflector = SelfReflection()
        self.refiner = GoalRefinement()

        self.brains = ["brain_00", "brain_01", "brain_02", "wink_brain"]
        self.running = True
        self.step = 0

    def features(self):
        val = random.random()
        self.temporal.update(val)
        return [val, self.temporal.predict_next()]

    def run_loop(self):
        print("[v22] UNIFIED OMEGA BRAIN ONLINE")

        while self.running:
            self.step += 1

            features = self.features()
            self.attention.add(features)

            focus = self.attention.get_focus()

            for brain in self.brains:
                score = self.model.predict(brain, features)

                decision = "optimize" if score > 0 else "explore"
                reward = random.random()

                # learning
                self.model.train(brain, features, reward)

                self.self_model.update(brain, reward)
                self.goals.update(brain, reward)

                state = self.reflector.reflect(self.self_model, brain)
                final_goal = self.refiner.refine(self.goals, state)

                print(f"[v22] {brain} | {decision} | goal={final_goal} | state={state}")

            self.model.save()
            time.sleep(2)


if __name__ == "__main__":
    OmegaUnifiedBrainV22().run_loop()
