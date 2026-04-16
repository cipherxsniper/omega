import math
import random
import json
from collections import deque

MODEL_FILE = "omega_ml_model.json"

class OmegaMLCoreV8:
    def __init__(self):
        self.data = deque(maxlen=1000)
        self.labels = deque(maxlen=1000)
        self.k = 3

        self.rewards = {}
        self.load_model()

    # ---------------------------
    # LOAD / SAVE
    # ---------------------------
    def save_model(self):
        with open(MODEL_FILE, "w") as f:
            json.dump({
                "data": list(self.data),
                "labels": list(self.labels),
                "rewards": self.rewards
            }, f)

    def load_model(self):
        try:
            with open(MODEL_FILE, "r") as f:
                m = json.load(f)
                self.data = deque(m["data"], maxlen=1000)
                self.labels = deque(m["labels"], maxlen=1000)
                self.rewards = m["rewards"]
        except:
            pass

    # ---------------------------
    # FEATURE EXTRACTION
    # ---------------------------
    def extract_features(self, memory):
        return [
            len(memory),
            sum([len(str(x)) for x in memory]) % 100,
            random.random()
        ]

    # ---------------------------
    # TRAIN (KNN)
    # ---------------------------
    def train(self, features, label):
        self.data.append(features)
        self.labels.append(label)

    def distance(self, a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    def predict(self, features):
        if len(self.data) < self.k:
            return random.choice(["explore", "exploit"])

        distances = []
        for i in range(len(self.data)):
            d = self.distance(features, self.data[i])
            distances.append((d, self.labels[i]))

        distances.sort(key=lambda x: x[0])
        top_k = [label for _, label in distances[:self.k]]

        return max(set(top_k), key=top_k.count)

    # ---------------------------
    # REINFORCEMENT
    # ---------------------------
    def reward(self, brain, value):
        self.rewards[brain] = self.rewards.get(brain, 0) + value

    def get_reward(self, brain):
        return self.rewards.get(brain, 0)

    # ---------------------------
    # DECISION ENGINE
    # ---------------------------
    def decide(self, brain, memory):
        features = self.extract_features(memory)
        decision = self.predict(features)

        # bias using rewards
        if self.get_reward(br

