import json
import os
import random
import math
import time
import requests
from collections import defaultdict


MODEL_FILE = "omega_swarm_shared_brain_v12.json"


# -----------------------------
# ACTIVATION
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dsigmoid(x):
    return x * (1 - x)


# -----------------------------
# 🌐 INTERNET INGESTION LAYER (v12)
# -----------------------------
class InternetIngestionV12:
    """
    Controlled real-world data ingestion layer.

    Pulls structured signals from:
    - crypto markets
    - public news feeds
    - optional APIs
    """

    def fetch_crypto(self):
        try:
            r = requests.get(
                "https://api.coindesk.com/v1/bpi/currentprice.json",
                timeout=4
            )
            price = r.json()["bpi"]["USD"]["rate_float"]
            return float(price)
        except:
            return random.uniform(20000, 70000)

    def fetch_news_signal(self):
        try:
            r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=4)
            text = r.text
            return len(text) % 1000
        except:
            return random.random() * 100

    def fetch_market_sentiment(self):
        # lightweight synthetic sentiment proxy
        return random.uniform(-1, 1)

    def get_features(self):
        return [
            self.fetch_crypto() / 100000,
            self.fetch_news_signal() / 1000,
            self.fetch_market_sentiment()
        ]


# -----------------------------
# 🧠 SWARM NEURAL CORE (v12 compatible with v11)
# -----------------------------
class OmegaMLCoreV12:
    """
    Swarm Shared Neural Brain + Internet ingestion
    """

    def __init__(self, input_size=6, hidden_size=8):
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.w1 = [[random.uniform(-1, 1) for _ in range(input_size)]
                   for _ in range(hidden_size)]

        self.w2 = [random.uniform(-1, 1) for _ in range(hidden_size)]

        self.b1 = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.b2 = random.uniform(-1, 1)

        self.lr = 0.03

        self.brain_influence = defaultdict(lambda: 1.0)

        self.ingestion = InternetIngestionV12()

        self.load_model()

    # -----------------------------
    # FEATURE COMBINATION
    # -----------------------------
    def encode(self, local_features, global_features):
        combined = local_features + global_features

        x = []
        for f in combined[:self.input_size]:
            try:
                x.append(float(f))
            except:
                x.append(random.random())

        while len(x) < self.input_size:
            x.append(0.0)

        return x

    # -----------------------------
    # FORWARD PASS
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
    # DECISION ENGINE (LOCAL + GLOBAL)
    # -----------------------------
    def decide(self, brain, memory):
        local = []

        for m in memory[-5:]:
            local.append(len(str(m)))

        if not local:
            local = [random.random() * 10]

        global_features = self.ingestion.get_features()

        x = self.encode(local, global_features)
        prediction = self.forward(x)

        if prediction > 0.5:
            return "optimize", x
        return "explore", x

    # -----------------------------
    # TRAIN SWARM (GLOBAL + LOCAL SIGNALS)
    # -----------------------------
    def train(self, brain, features, decision):
        target = 1.0 if decision == "optimize" else 0.0

        error = target - self.output
        d_output = error * dsigmoid(self.output)

        influence = self.brain_influence[brain]

        hidden_errors = [0] * self.hidden_size

        for i in range(self.hidden_size):
            hidden_errors[i] = self.w2[i] * d_output

        for i in range(self.hidden_size):
            self.w2[i] += self.lr * d_output * self.hidden[i] * influence

        self.b2 += self.lr * d_output * influence

        for i in range(self.hidden_size):
            d_hidden = hidden_errors[i] * dsigmoid(self.hidden[i])

            for j in range(self.input_size):
                self.w1[i][j] += self.lr * d_hidden * features[j] * influence

            self.b1[i] += self.lr * d_hidden * influence

        if decision == "optimize":
            self.brain_influence[brain] += 0.001
        else:
            self.brain_influence[brain] *= 0.999

    # -----------------------------
    # REWARD SIGNAL
    # -----------------------------
    def reward(self, brain, reward_value):
        bias = reward_value - 0.5
        self.b2 += self.lr * bias * 0.01

    # -----------------------------
    # SAVE / LOAD
    # -----------------------------

    # -----------------------------
    # SAVE / LOAD
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

                print("[ML V12] Loaded")
            except Exception as e:
                print("[ML V12] Load failed:", e)

# -----------------------------

# -----------------------------
# BOOT STRAP
# -----------------------------
if __name__ == "__main__":
    print("[ML V12] Starting Omega ML Core...")

    ml = OmegaMLCoreV12()

    import random
    import time

    brain = "brain_00"

    while True:
        mem = [{"data": random.random()} for _ in range(5)]

        decision, features = ml.decide(brain, mem)
        reward = random.random()

        ml.reward(brain, reward)

        # FIXED LINE (match function signature)
        ml.train(brain, features, decision)

        print(f"[ML V12] {brain} → {decision} | reward={reward:.3f}")

        time.sleep(2)
