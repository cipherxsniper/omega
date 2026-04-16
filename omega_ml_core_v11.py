import json
import os
import math
import random
from collections import defaultdict

MODEL_FILE = "omega_swarm_shared_brain_v11.json"


# -----------------------------
# ACTIVATION FUNCTIONS
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dsigmoid(x):
    return x * (1 - x)


# -----------------------------
# 🧠 SWARM SHARED BRAIN v11
# -----------------------------
class OmegaMLCoreV11:
    """
    Shared Swarm Neural Brain (v11)

    CORE IDEA:
    - ONE neural network for ALL brains
    - Each brain contributes to shared learning
    - Global memory convergence
    """

    def __init__(self, input_size=5, hidden_size=8):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # 🧠 SINGLE SHARED NETWORK (GLOBAL SWARM BRAIN)
        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)]
                   for _ in range(hidden_size)]

        self.w2 = [random.uniform(-1, 1) for _ in range(hidden_size)]

        self.b1 = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.b2 = random.uniform(-1, 1)

        self.lr = 0.04

        # swarm memory weighting
        self.brain_influence = defaultdict(lambda: 1.0)

        self.load_model()

    # -----------------------------
    # FEATURE ENCODING
    # -----------------------------
    def encode(self, features):
        x = []

        for f in features[:self.input_size]:
            try:
                x.append(float(f) / 100.0)
            except:
                x.append(random.random())

        while len(x) < self.input_size:
            x.append(0.0)

        return x

    # -----------------------------
    # FORWARD PASS (SHARED BRAIN)
    # -----------------------------
    def forward(self, x):
        self.hidden = []

        for i in range(self.hidden_size):
            val = self.b1[i]

            for j in range(self.input_size):
                val += self.w1[i][j] * x[j]

            self.hidden.append(sigmoid(val))

        out = self.b2

        for i in range(self.hidden_size):
            out += self.w2[i] * self.hidden[i]

        self.output = sigmoid(out)

        return self.output

    # -----------------------------
    # DECISION (PER BRAIN, SAME MODEL)
    # -----------------------------
    def decide(self, brain, memory):
        features = []

        for m in memory[-5:]:
            if isinstance(m, dict):
                features.append(len(str(m.get("data", ""))))
            else:
                features.append(len(str(m)))

        if not features:
            features = [random.random() * 100]

        x = self.encode(features)
        prediction = self.forward(x)

        if prediction > 0.5:
            return "optimize", x
        else:
            return "explore", x

    # -----------------------------
    # SWARM TRAINING (GLOBAL UPDATE)
    # -----------------------------
    def train(self, brain, features, decision):
        target = 1.0 if decision == "optimize" else 0.0

        error = target - self.output
        d_output = error * dsigmoid(self.output)

        # 🧠 adjust influence per brain (swarm identity weighting)
        influence = self.brain_influence[brain]

        # hidden error propagation
        hidden_errors = [0] * self.hidden_size

        for i in range(self.hidden_size):
            hidden_errors[i] = self.w2[i] * d_output

        # update output layer
        for i in range(self.hidden_size):
            self.w2[i] += self.lr * d_output * self.hidden[i] * influence

        self.b2 += self.lr * d_output * influence

        # update hidden layer
        for i in range(self.hidden_size):
            d_hidden = hidden_errors[i] * dsigmoid(self.hidden[i])

            for j in range(self.input_size):
                self.w1[i][j] += self.lr * d_hidden * features[j] * influence

            self.b1[i] += self.lr * d_hidden * influence

        # strengthen brain influence if correct behavior
        if decision == "optimize":
            self.brain_influence[brain] += 0.001
        else:
            self.brain_influence[brain] *= 0.999

    # -----------------------------
    # REWARD FEEDBACK (SWARM ALIGNMENT)
    # -----------------------------
    def reward(self, brain, reward_value):
        bias = reward_value - 0.5

        self.b2 += self.lr * bias * 0.01
        self.brain_influence[brain] += bias * 0.001

    # -----------------------------
    # SAVE MODEL
    # -----------------------------
    def save_model(self):
        data = {
            "w1": self.w1,
            "w2": self.w2,
            "b1": self.b1,
            "b2": self.b2,
            "brain_influence": dict(self.brain_influence)
        }

        with open(MODEL_FILE, "w") as f:
            json.dump(data, f)

    # -----------------------------
    # LOAD MODEL
    # -----------------------------
    def load_model(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                self.w1 = data["w1"]
                self.w2 = data["w2"]
                self.b1 = data["b1"]
                self.b2 = data["b2"]
                self.brain_influence.update(data.get("brain_influence", {}))

                print("[ML V11] Shared swarm brain loaded")
            except:
                print("[ML V11] Failed load → fresh swarm brain")
        else:
            print("[ML V11] No swarm model → initializing new shared brain")
