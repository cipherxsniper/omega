import os
import time
import json
import math
import random
import threading
import urllib.request
from collections import deque

# ---------------------------
# FILES
# ---------------------------
MODEL_FILE = "omega_shared_nn.json"
MEMORY_FILE = "omega_mesh_memory.json"
CODE_BACKUP = "omega_code_backup_v12.py"

# ---------------------------
# 🧠 SHARED NEURAL NETWORK
# ---------------------------
class SharedNeuralNet:
    def __init__(self):
        self.input_size = 4
        self.hidden_size = 8
        self.output_size = 2

        self.w1 = [[random.uniform(-1,1) for _ in range(self.hidden_size)] for _ in range(self.input_size)]
        self.w2 = [[random.uniform(-1,1) for _ in range(self.output_size)] for _ in range(self.hidden_size)]

        self.load()

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

    def mutate(self, strength=0.1):
        for layer in [self.w1, self.w2]:
            for i in range(len(layer)):
                for j in range(len(layer[i])):
                    if random.random() < 0.15:
                        layer[i][j] += random.uniform(-strength, strength)

    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump({"w1": self.w1, "w2": self.w2}, f)

    def load(self):
        try:
            with open(MODEL_FILE, "r") as f:
                data = json.load(f)
                self.w1 = data["w1"]
                self.w2 = data["w2"]
        except:
            pass


# ---------------------------
# 🌐 DATA INGESTION LAYER
# ---------------------------
class DataIngestion:
    def fetch_time(self):
        try:
            with urllib.request.urlopen("http://worldtimeapi.org/api/timezone/Etc/UTC", timeout=5) as r:
                return json.loads(r.read().decode())
        except:
            return {}

    def fetch_crypto(self):
        try:
            with urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=5) as r:
                return json.loads(r.read().decode())
        except:
            return {}

    def get_all(self):
        return {
            "time": self.fetch_time(),
            "crypto": self.fetch_crypto()
        }


# ---------------------------
# 🧬 SELF-EVOLUTION ENGINE
# ---------------------------
class CodeEvolution:
    def mutate_code(self):
        try:
            with open(__file__, "r") as f:
                code = f.read()

            with open(CODE_BACKUP, "w") as f:
                f.write(code)

            mutation = f"\n# evolved_{random.randint(1000,9999)}"

            with open(__file__, "a") as f:
                f.write(mutation)

        except Exception as e:
            print("[EVOLUTION ERROR]", e)


# ---------------------------
# 🧠 MESH NODE (BRAIN)
# ---------------------------
class MeshBrain:
    def __init__(self, name, nn, memory):
        self.name = name
        self.nn = nn
        self.memory = memory
        self.local_memory = deque(maxlen=200)
        self.reward = 0

    def extract_features(self, global_data):
        return [
            len(self.local_memory),
            len(self.memory),
            random.random(),
            len(str(global_data)) % 100
        ]

    def act(self, global_data):
        features = self.extract_features(global_data)
        out = self.nn.forward(features)

        decision = "explore" if out[0] > out[1] else "exploit"

        entry = {
            "brain": self.name,
            "decision": decision,
            "t": time.time()
        }

        self.local_memory.append(entry)
        self.memory.append(entry)

        # reward system
        r = random.uniform(0.1, 1.0)
        self.reward += r

        return decision, r


# ---------------------------
# 🚀 MAIN SYSTEM
# ---------------------------
class OmegaMeshV12:
    def __init__(self):
        self.nn = SharedNeuralNet()
        self.ingest = DataIngestion()
        self.evolver = CodeEvolution()

        self.memory = deque(maxlen=2000)

        self.brains = [
            MeshBrain("brain_00", self.nn, self.memory),
            MeshBrain("brain_01", self.nn, self.memory),
            MeshBrain("brain_02", self.nn, self.memory),
            MeshBrain("brain_wink", self.nn, self.memory),
        ]

        self.running = True

    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(list(self.memory), f)

    def loop(self):
        cycle = 0

        while self.running:
            try:
                cycle += 1

                # 🌐 ingest real data
                data = self.ingest.get_all()

                top_brain = None
                top_reward = -1

                for brain in self.brains:
                    decision, reward = brain.act(data)

                    if reward > top_reward:
                        top_reward = reward
                        top_brain = brain.name

                # 🧠 evolve neural net
                if top_reward > 0.7:
                    self.nn.mutate()

                self.nn.save()
                self.save_memory()

                # 🧬 evolve code occasionally
                if random.random() < 0.03:
                    self.evolver.mutate_code()

                print(f"[V12] Cycle {cycle} | TOP: {top_brain} | Reward: {top_reward:.3f}")

            except Exception as e:
                print("[ERROR]", e)

            time.sleep(2)


# ---------------------------
# ENTRY
# ---------------------------
if __name__ == "__main__":
    OmegaMeshV12().loop()

# evolved_1711
# evolved_7367
# evolved_3196
# evolved_4901
# evolved_4273
# evolved_2259
# evolved_4217