import os
import time
import json
import math
import random
import urllib.request
import threading
from collections import deque

MODEL_FILE = "omega_nn_model.json"
CODE_BACKUP = "omega_code_backup.py"

# ---------------------------
# SIMPLE NEURAL NETWORK
# ---------------------------
class SimpleNeuralNet:
    def __init__(self):
        self.input_size = 3
        self.hidden_size = 6
        self.output_size = 2

        self.w1 = [[random.uniform(-1,1) for _ in range(self.hidden_size)] for _ in range(self.input_size)]
        self.w2 = [[random.uniform(-1,1) for _ in range(self.output_size)] for _ in range(self.hidden_size)]

    def activate(self, x):
        return 1 / (1 + math.exp(-x))

    def forward(self, inputs):
        hidden = [
            self.activate(sum(inputs[i] * self.w1[i][j] for i in range(self.input_size)))
            for j in range(self.hidden_size)
        ]

        output = [
            self.activate(sum(hidden[j] * self.w2[j][k] for j in range(self.hidden_size)))
            for k in range(self.output_size)
        ]

        return output

    def mutate(self):
        for i in range(len(self.w1)):
            for j in range(len(self.w1[i])):
                if random.random() < 0.1:
                    self.w1[i][j] += random.uniform(-0.2, 0.2)

        for i in range(len(self.w2)):
            for j in range(len(self.w2[i])):
                if random.random() < 0.1:
                    self.w2[i][j] += random.uniform(-0.2, 0.2)


# ---------------------------
# SUPER INTELLIGENCE CORE
# ---------------------------
class OmegaSuperIntelligenceV9:
    def __init__(self):
        self.nn = SimpleNeuralNet()
        self.memory = deque(maxlen=1000)
        self.rewards = {}

        self.running = True

    # ---------------------------
    # FEATURE EXTRACTION
    # ---------------------------
    def extract_features(self):
        return [
            len(self.memory),
            sum(len(str(x)) for x in self.memory) % 100,
            random.random()
        ]

    # ---------------------------
    # DECISION
    # ---------------------------
    def decide(self):
        features = self.extract_features()
        output = self.nn.forward(features)

        return "explore" if output[0] > output[1] else "exploit"

    # ---------------------------
    # REWARD SYSTEM
    # ---------------------------
    def reward(self, key, value):
        self.rewards[key] = self.rewards.get(key, 0) + value

    # ---------------------------
    # 🌐 INTERNET INGESTION
    # ---------------------------
    def fetch_data(self):
        try:
            url = "http://worldtimeapi.org/api/timezone/Etc/UTC"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())

                self.memory.append(data)
                return data
        except:
            return None

    # ---------------------------
    # 🧬 SELF-CODE EVOLUTION (SAFE)
    # ---------------------------
    def evolve_code(self):
        try:
            with open(__file__, "r") as f:
                code = f.read()

            # backup
            with open(CODE_BACKUP, "w") as f:
                f.write(code)

            # simple mutation: add comment (safe)
            mutation = f"\n# mutation {random.randint(0,9999)}"

            with open(__file__, "a") as f:
                f.write(mutation)

        except Exception as e:
            print("Evolution error:", e)

    # ---------------------------
    # LEARNING LOOP
    # ---------------------------
    def loop(self):
        while self.running:
            try:
                # 🌐 fetch real-world data
                data = self.fetch_data()

                decision = self.decide()

                if decision == "explore":
                    self.memory.append({"action": "explore", "t": time.time()})
                    reward = random.uniform(0.1, 0.5)
                else:
                    self.memory.append({"action": "exploit", "t": time.time()})
                    reward = random.uniform(0.5, 1.0)

                self.reward("global", reward)

                # 🧠 evolve neural network
                if reward > 0.7:
                    self.nn.mutate()

                # 🧬 occasional self evolution
                if random.random() < 0.05:
                    self.evolve_code()

                print(f"[V9] Decision: {decision} | Reward: {reward:.3f} | Memory: {len(self.memory)}")

            except Exception as e:
                print("[V9 ERROR]", e)

            time.sleep(2)


# ---------------------------
# ENTRY
# ---------------------------
if __name__ == "__main__":
    omega = OmegaSuperIntelligenceV9()
    omega.loop()

# mutation 636
# mutation 1166
# mutation 5582
# mutation 6874
# mutation 8649
# mutation 4196
# mutation 2547
# mutation 6046
# mutation 9388
# mutation 3645
# mutation 4334
# mutation 9736
# mutation 7959
# mutation 1351
# mutation 1577
# mutation 4322
# mutation 2828
# mutation 6061
# mutation 1102
# mutation 8725
# mutation 7978
# mutation 6006
# mutation 6948
# mutation 6627
# mutation 9891
# mutation 4471
# mutation 6815
# mutation 177
# mutation 4428
# mutation 142
# mutation 1309
# mutation 3705
# mutation 1417
# mutation 2481
# mutation 9951
# mutation 9666
# mutation 9246
# mutation 1209
# mutation 4311
# mutation 3069
# mutation 5654
# mutation 6837
# mutation 557
# mutation 1791
# mutation 1318
# mutation 5524
# mutation 5228
# mutation 7028
# mutation 4156