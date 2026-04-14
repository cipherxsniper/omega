import os
import json
import time
import math
import random
import fcntl

SHARED_MEMORY_FILE = "omega_cross_memory.json"
LOCK_FILE = "omega_cross_memory.lock"


class CrossProcessMemory:
    def __init__(self, path=SHARED_MEMORY_FILE):
        self.path = path
        self.init_store()

    def init_store(self):
        if not os.path.exists(self.path):
            data = {
                "global_memory": [],
                "brain_history": {},
                "last_step": 0
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


class OmegaAdaptiveConvergenceV17:
    def __init__(self, brains, instance_id=None):
        self.brains = brains
        self.instance_id = instance_id or f"omega_{random.randint(1000,9999)}"

        self.memory = CrossProcessMemory()

        self.state = self.memory.read()

        self.scores = {b: 1.0 for b in brains}
        self.step = self.state.get("last_step", 0)

        self.decay = 0.90
        self.noise = 0.03
        self.memory_weight = 0.18
        self.max_cap = 1e6

    # ---------------- CORE SAFETY ----------------

    def stabilize(self, v):
        if v > self.max_cap:
            v = math.log(v + 1)
        if v < 1e-9:
            v = 1e-9
        return v

    def normalize(self):
        total = sum(self.scores.values())
        if total == 0:
            return
        for k in self.scores:
            self.scores[k] /= total

    # ---------------- CROSS PROCESS MEMORY ----------------

    def sync_memory(self):
        """Pull latest global state from disk"""
        self.state = self.memory.read()

    def push_memory(self, top_brain):
        """Write this instance experience into shared memory"""

        event = {
            "ts": time.time(),
            "instance": self.instance_id,
            "step": self.step,
            "top": top_brain,
            "snapshot": dict(self.scores)
        }

        self.state["global_memory"].append(event)

        # keep bounded memory
        self.state["global_memory"] = self.state["global_memory"][-300:]

        self.state["last_step"] = self.step

        # brain history fusion
        hist = self.state.get("brain_history", {})
        hist.setdefault(top_brain, 0)
        hist[top_brain] += 1
        self.state["brain_history"] = hist

        self.memory.write(self.state)

    def memory_bias(self, brain):
        hist = self.state.get("brain_history", {})
        if brain not in hist:
            return 1.0
        return 1.0 + (hist[brain] * self.memory_weight)

    # ---------------- EVOLUTION ----------------

    def step_once(self):
        self.sync_memory()
        self.step += 1

        global_pressure = sum(self.scores.values()) / len(self.scores)

        new_scores = {}

        for b in self.brains:
            noise = random.random() * self.noise
            mem = self.memory_bias(b)

            current = self.scores[b]

            growth = (
                current
                * (1 + noise)
                * self.decay
                * mem
                * (1 + global_pressure * 0.05)
            )

            new_scores[b] = self.stabilize(growth)

        self.scores = new_scores
        self.normalize()

        top = max(self.scores, key=self.scores.get)

        self.push_memory(top)

        return {
            "instance": self.instance_id,
            "step": self.step,
            "top": top,
            "scores": self.scores
        }


# ---------------- DAEMON LOOP ----------------

def run_daemon():
    omega = OmegaAdaptiveConvergenceV17(
        brains=["brain_0", "brain_1", "brain_2", "brain_3"]
    )

    print(f"[OMEGA v17] CROSS-PROCESS NETWORK ONLINE | {omega.instance_id}")

    while True:
        try:
            result = omega.step_once()

            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"STEP {result['step']} | TOP: {result['top']} | "
                f"INST: {result['instance']}"
            )

            time.sleep(0.2)

        except KeyboardInterrupt:
            print("[OMEGA v17] SHUTDOWN")
            break

        except Exception as e:
            print("[OMEGA v17 ERROR]", str(e))
            time.sleep(1.5)


if __name__ == "__main__":
    run_daemon()

# OPTIMIZED BY v29 ENGINE
