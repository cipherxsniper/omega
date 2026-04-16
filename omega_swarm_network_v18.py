import os
import json
import time
import math
import random
import socket
import fcntl
from threading import Thread

MEM_FILE = "omega_swarm_state.json"
LOCK_FILE = "omega_swarm.lock"

# -------------------------
# SWARM STATE MANAGER
# -------------------------

class SwarmState:
    def __init__(self, path=MEM_FILE):
        self.path = path
        self.init()

    def init(self):
        if not os.path.exists(self.path):
            data = {
                "nodes": {},
                "global_memory": [],
                "step": 0,
                "leader": None
            }
            with open(self.path, "w") as f:
                json.dump(data, f)

    def _lock(self, f):
        fcntl.flock(f, fcntl.LOCK_EX)

    def _unlock(self, f):
        fcntl.flock(f, fcntl.LOCK_UN)

    def read(self):
        with open(self.path, "r") as f:
            self._lock(f)
            data = json.load(f)
            self._unlock(f)
        return data

    def write(self, data):
        with open(self.path, "r+") as f:
            self._lock(f)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            self._unlock(f)


# -------------------------
# SWARM NODE
# -------------------------

class OmegaSwarmNodeV18:
    def __init__(self, brains, role="worker"):
        self.id = f"node_{random.randint(1000,9999)}"
        self.role = role
        self.state = SwarmState()

        self.brains = brains
        self.scores = {b: 1.0 for b in brains}

        self.step = 0

        self.decay = 0.91
        self.noise = 0.03
        self.memory_weight = 0.2

        self.alive = True

    # -------------------------
    # NODE REGISTRATION
    # -------------------------

    def register(self):
        data = self.state.read()

        data["nodes"][self.id] = {
            "role": self.role,
            "last_seen": time.time(),
            "score": 1.0
        }

        # leader election (simplified)
        if data["leader"] is None:
            data["leader"] = self.id

        self.state.write(data)

    # -------------------------
    # HEARTBEAT
    # -------------------------

    def heartbeat(self):
        while self.alive:
            data = self.state.read()

            if self.id in data["nodes"]:
                data["nodes"][self.id]["last_seen"] = time.time()
                data["nodes"][self.id]["score"] = sum(self.scores.values())

            self.state.write(data)
            time.sleep(1)

    # -------------------------
    # LEADER CHECK
    # -------------------------

    def is_leader(self):
        data = self.state.read()
        return data.get("leader") == self.id

    # -------------------------
    # MEMORY FUSION
    # -------------------------

    def global_bias(self, brain):
        data = self.state.read()
        mem = data.get("global_memory", [])

        count = sum(1 for m in mem if m.get("top") == brain)

        return 1.0 + (count * self.memory_weight)

    # -------------------------
    # SWARM STEP
    # -------------------------

    def step_once(self):
        data = self.state.read()
        self.step += 1

        global_pressure = sum(self.scores.values()) / len(self.scores)

        new_scores = {}

        for b in self.brains:
            noise = random.random() * self.noise
            bias = self.global_bias(b)

            current = self.scores[b]

            growth = (
                current
                * (1 + noise)
                * self.decay
                * bias
                * (1 + global_pressure * 0.05)
            )

            new_scores[b] = max(1e-9, growth)

        self.scores = self.normalize(new_scores)

        top = max(self.scores, key=self.scores.get)

        # ONLY leader writes consensus memory
        if self.is_leader():
            data["global_memory"].append({
                "ts": time.time(),
                "node": self.id,
                "step": self.step,
                "top": top,
                "snapshot": dict(self.scores)
            })

            data["global_memory"] = data["global_memory"][-500:]

            data["step"] = self.step

            self.state.write(data)

        return top

    def normalize(self, scores):
        total = sum(scores.values())
        if total == 0:
            return scores
        return {k: v / total for k, v in scores.items()}

    # -------------------------
    # RUN LOOP
    # -------------------------

    def run(self):
        self.register()

        Thread(target=self.heartbeat, daemon=True).start()

        print(f"[OMEGA v18] SWARM NODE ONLINE | {self.id} | ROLE: {self.role}")

        while self.alive:
            try:
                top = self.step_once()

                print(
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"NODE:{self.id} | TOP:{top} | ROLE:{self.role}"
                )

                time.sleep(0.2)

            except Exception as e:
                print("[SWARM ERROR]", e)
                time.sleep(1)


# -------------------------
# BOOT SWARM
# -------------------------

if __name__ == "__main__":
    brains = ["brain_0", "brain_1", "brain_2", "brain_3"]

    role = os.environ.get("OMEGA_ROLE", "worker")

    node = OmegaSwarmNodeV18(brains, role=role)
    node.run()
