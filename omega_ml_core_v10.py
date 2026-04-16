import json
import os
import math
import random
from collections import defaultdict

MODEL_FILE = "omega_ml_core_v10_model.json"


# -----------------------------
# 🔥 ACTIVATION FUNCTION
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dsigmoid(x):
    return x * (1 - x)


# -----------------------------
# 🧠 NEURAL CORE V10
# -----------------------------
class OmegaMLCoreV10:
    """
    Real lightweight neural network core for Omega swarm.

    Architecture:
    Input Layer → Hidden Layer → Output Decision
    Includes:
    - Forward propagation
    - Backpropagation
    - Swarm-compatible brain weighting
    """

    def __init__(self, input_size=5, hidden_size=6):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # weights
        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)]
                   for _ in range(hidden_size)]

        self.w2 = [random.uniform(-1, 1) for _ in range(hidden_size)]

        # biases
        self.b1 = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.b2 = random.uniform(-1, 1)

        self.lr = 0.05

        self.load_model()

    # -----------------------------
    # FEATURE ENCODING
    # -----------------------------
    def encode(self, features):
        out = []

        for f in features[:self.input_size]:
            try:
                out.append(float(f) / 100.0)
            except:
                out.append(random.random())

        while len(out) < self.input_size:
            out.append(0.0)

        return out

    # -----------------------------
    # FORWARD PASS
    # -----------------------------
    def forward(self, x):
        self.hidden = []

        for i in range(self.hidden_size):
            activation = self.b1[i]

            for j in range(self.input_size):
                activation += self.w1[i][j] * x[j]

            self.hidden.append(sigmoid(activation))

        output = self.b2

        for i in range(self.hidden_size):
            output += self.w2[i] * self.hidden[i]

        self.output = sigmoid(output)

        return self.output

    # -----------------------------
    # DECISION ENGINE
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
    # BACKPROP LEARNING
    # -----------------------------
    def train(self, features, decision):
        target = 1.0 if decision == "optimize" else 0.0

        error = target - self.output
        d_output = error * dsigmoid(self.output)

        # hidden layer gradients
        hidden_errors = [0] * self.hidden_size

        for i in range(self.hidden_size):
            hidden_errors[i] = self.w2[i] * d_output

        # update w2 + b2
        for i in range(self.hidden_size):
            self.w2[i] += self.lr * d_output * self.hidden[i]

        self.b2 += self.lr * d_output

        # update w1 + b1
        for i in range(self.hidden_size):
            d_hidden = hidden_errors[i] * dsigmoid(self.hidden[i])

            for j in range(self.input_size):
                self.w1[i][j] += self.lr * d_hidden * features[j]

            self.b1[i] += self.lr * d_hidden

    # -----------------------------
    # REWARD (SWARM FEEDBACK)
    # -----------------------------
    def reward(self, brain, reward_value):
        # subtle reinforcement bias per brain
        bias = reward_value - 0.5

        self.b2 += self.lr * bias * 0.01

    # -----------------------------
    # SAVE MODEL
    # -----------------------------
    def save_model(self):
        data = {
            "w1": self.w1,
            "w2": self.w2,
            "b1": self.b1,
            "b2": self.b2
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

                print("[ML V10] Neural model loaded")
            except:
                print("[ML V10] Failed to load model — initializing fresh network")
        else:
            print("[ML V10] No model found — initializing fresh network")
