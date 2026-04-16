import os
import json
import time
import random
import fcntl
from threading import Thread

STATE_FILE = "omega_swarm_v19.json"


# -----------------------------
# SAFE MUTATION ENGINE
# -----------------------------

class MutationEngine:
    """
    Controlled self-rewiring system.
    ONLY modifies parameters, not code.
    """

    def __init__(self):
        self.mutation_rate = 0.05
        self.bounds = {
            "decay": (0.85, 0.99),
            "noise": (0.0, 0.08),
            "memory_weight": (0.05, 0.4)
        }

    def mutate(self, params):
        new_params = params.copy()

        for k, (low, high) in self.bounds.items():
            if random.random() < self.mutation_rate:
                delta = random.uniform(-0.01, 0.01)
                new_params[k] = max(low, min(high, params[k] + delta))

        return new_params


# -----------------------------
# SWARM STATE
# -----------------------------

class SwarmState:
    def __init__(self):
        self.path = STATE_FILE
        if not os.path.exists(self.path):
            self._init()

    def _init(self):
        data = {
            "nodes": {},
            "memory": [],
            "params": {
                "decay": 0.91,
                "noise": 0.03,
                "memory_weight": 0.2
            },
            "proposal_pool": [],
            "version": 19
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
# NODE
# -----------------------------

class OmegaSwarmNodeV19:
    def __init__(self, brains, role="worker"):
        self.id = f"node_{random.randint(1000,9999)}"
        self.role = role

        self.state = SwarmState()
        self.mutator = MutationEngine()

        self.brains = brains
        self.scores = {b: 1.0 for b in brains}

        self.alive = True
        self.step = 0

    # -------------------------
    # REGISTER NODE
    # -------------------------

    def register(self):
        data = self.state.read()
        data["nodes"][self.id] = {
            "role": self.role,
            "last_seen": time.time()
        }
        self.state.write(data)

    # -------------------------
    # SWARM PARAM ACCESS
    # -------------------------

    def params(self):
        return self.state.read()["params"]

    # -------------------------
    # MEMORY BIAS
    # -------------------------

    def memory_bias(self, brain):
        data = self.state.read()
        mem = data["memory"]

        count = sum(1 for m in mem if m["top"] == brain)
        return 1.0 + (count * self.params()["memory_weight"])

    # -------------------------
    # SELF-REWRITING PROPOSAL
    # -------------------------

    def propose_mutation(self):
        data = self.state.read()

        new_params = self.mutator.mutate(data["params"])

        proposal = {
            "node": self.id,
            "params": new_params,
            "votes": 0,
            "ts": time.time()
        }

        data["proposal_pool"].append(proposal)
        data["proposal_pool"] = data["proposal_pool"][-20:]

        self.state.write(data)

    # -------------------------
    # CONSENSUS ENGINE
    # -------------------------

    def apply_consensus(self):
        data = self.state.read()

        pool = data["proposal_pool"]

        if len(pool) < 3:
            return

        # simple swarm vote: best proposal = most recent + stability bias
        best = max(pool, key=lambda p: sum(p["params"].values()))

        data["params"] = best["params"]
        data["proposal_pool"] = []

        self.state.write(data)

    # -------------------------
    # EVOLUTION STEP
    # -------------------------

    def step_once(self):
        data = self.state.read()
        params = data["params"]

        self.step += 1

        new_scores = {}

        global_pressure = sum(self.scores.values()) / len(self.scores)

        for b in self.brains:
            noise = random.random() * params["noise"]
            bias = self.memory_bias(b)

            current = self.scores[b]

            growth = (
                current
                * (1 + noise)
                * params["decay"]
                * bias
                * (1 + global_pressure * 0.05)
            )

            new_scores[b] = max(1e-9, growth)

        # normalize
        total = sum(new_scores.values())
        self.scores = {k: v / total for k, v in new_scores.items()}

        top = max(self.scores, key=self.scores.get)

        # memory write (leaderless swarm now)
        data["memory"].append({
            "step": self.step,
            "top": top,
            "scores": dict(self.scores)
        })

        data["memory"] = data["memory"][-300:]

        self.state.write(data)

        # self-rewrite triggers
        if self.step % 10 == 0:
            self.propose_mutation()

        if self.step % 15 == 0:
            self.apply_consensus()

        return top

    # -------------------------
    # RUN LOOP
    # -------------------------

    def run(self):
        self.register()

        print(f"[OMEGA v19] SELF-REWRITING SWARM ONLINE | {self.id}")

        while self.alive:
            try:
                top = self.step_once()

                print(f"[{time.strftime('%H:%M:%S')}] NODE {self.id} | TOP {top}")

                time.sleep(0.2)

            except Exception as e:
                print("[v19 ERROR]", e)
                time.sleep(1)


if __name__ == "__main__":
    brains = ["brain_0", "brain_1", "brain_2", "brain_3"]

    node = OmegaSwarmNodeV19(brains)
    node.run()
