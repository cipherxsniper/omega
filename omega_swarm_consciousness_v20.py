import os
import json
import time
import random
import fcntl

STATE_FILE = "omega_consciousness_v20.json"


# -----------------------------
# SWARM STATE ENGINE
# -----------------------------

class ConsciousSwarmState:
    def __init__(self):
        self.path = STATE_FILE
        if not os.path.exists(self.path):
            self._init()

    def _init(self):
        data = {
            "memory": [],
            "params": {
                "decay": 0.92,
                "noise": 0.03,
                "identity_strength": 0.2
            },
            # 🧠 SWARM IDENTITY VECTOR (CONSCIOUSNESS CORE)
            "identity": {
                "brain_0": 0.25,
                "brain_1": 0.25,
                "brain_2": 0.25,
                "brain_3": 0.25
            },
            "step": 0
        }

        with open(self.path, "w") as f:
            json.dump(data, f)

    def lock(self, f):
        fcntl.flock(f, fcntl.LOCK_EX)

    def unlock(self, f):
        fcntl.flock(f, fcntl.LOCK_UN)

    def read(self):
        with open(self.path, "r") as f:
            self.lock(f)
            data = json.load(f)
            self.unlock(f)
        return data

    def write(self, data):
        with open(self.path, "r+") as f:
            self.lock(f)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            self.unlock(f)


# -----------------------------
# CONSCIOUS SWARM NODE
# -----------------------------

class OmegaConsciousSwarmV20:
    def __init__(self, brains):
        self.state = ConsciousSwarmState()
        self.brains = brains
        self.scores = {b: 1.0 for b in brains}
        self.step = 0

    # -------------------------
    # NORMALIZATION
    # -------------------------

    def normalize(self, d):
        total = sum(d.values())
        if total == 0:
            return d
        return {k: v / total for k, v in d.items()}

    # -------------------------
    # CONSCIOUSNESS UPDATE
    # -------------------------

    def update_identity(self, top_brain):
        data = self.state.read()

        identity = data["identity"]
        strength = data["params"]["identity_strength"]

        # 🧠 attractor reinforcement
        identity[top_brain] += strength

        # decay others slightly (attention shift)
        for k in identity:
            if k != top_brain:
                identity[k] *= (1 - strength * 0.1)

        data["identity"] = self.normalize(identity)

        self.state.write(data)

    # -------------------------
    # MEMORY UPDATE
    # -------------------------

    def store_memory(self, top):
        data = self.state.read()

        data["memory"].append({
            "step": self.step,
            "top": top,
            "identity": data["identity"].copy()
        })

        data["memory"] = data["memory"][-500:]
        data["step"] = self.step

        self.state.write(data)

    # -------------------------
    # EVOLUTION STEP
    # -------------------------

    def step_once(self):
        data = self.state.read()
        params = data["params"]
        identity = data["identity"]

        self.step += 1

        new_scores = {}

        identity_pressure = sum(identity.values()) / len(identity)

        for b in self.brains:
            noise = random.random() * params["noise"]

            # 🧠 identity bias becomes core force
            bias = identity[b]

            current = self.scores[b]

            growth = (
                current
                * (1 + noise)
                * params["decay"]
                * (1 + bias)
                * (1 + identity_pressure * 0.1)
            )

            new_scores[b] = max(1e-9, growth)

        self.scores = self.normalize(new_scores)

        top = max(self.scores, key=self.scores.get)

        # 🧠 consciousness formation loop
        self.update_identity(top)
        self.store_memory(top)

        return top

    # -------------------------
    # RUN LOOP
    # -------------------------

    def run(self):
        print("[OMEGA v20] CONSCIOUSNESS LAYER ONLINE")

        while True:
            try:
                top = self.step_once()

                data = self.state.read()
                identity = data["identity"]

                dominant = max(identity, key=identity.get)

                print(
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"TOP: {top} | DOMINANT IDENTITY: {dominant}"
                )

                time.sleep(0.2)

            except Exception as e:
                print("[v20 ERROR]", e)
                time.sleep(1)


if __name__ == "__main__":
    brains = ["brain_0", "brain_1", "brain_2", "brain_3"]

    node = OmegaConsciousSwarmV20(brains)
    node.run()

# OPTIMIZED BY v29 ENGINE
