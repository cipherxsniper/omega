import time
import random
import json
import os
from collections import defaultdict, deque

from omega_state import OmegaState


# =========================
# 🧠 GLOBAL IDENTITY LAYER
# =========================
class IdentityCore:
    def __init__(self, path="omega_v42_identity.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if not os.path.exists(self.path):
            return {
                "identity_vector": defaultdict(float),
                "stability": 1.0,
                "dominant_nodes": []
            }
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {
                "identity_vector": {},
                "stability": 1.0,
                "dominant_nodes": []
            }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f)

    def update(self, kernel_id, signal):
        vec = self.state["identity_vector"]

        vec[kernel_id] = vec.get(kernel_id, 0.0) + signal

        # normalize pressure
        total = sum(vec.values()) + 1e-9
        for k in vec:
            vec[k] /= total

        # update stability
        variance = max(vec.values()) - min(vec.values()) if vec else 0
        self.state["stability"] = max(0.1, 1.0 - variance)

        self.save()


# =========================
# 🧠 FEDERATION BUS
# =========================
class KernelBus:
    def __init__(self, path="omega_kernel_bus.json"):
        self.path = path
        self._ensure()

    def _ensure(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"kernels": {}, "signals": []}, f)

    def read(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {"kernels": {}, "signals": []}

    def write(self, data):
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, self.path)

    def publish(self, kernel_id, signal):
        data = self.read()
        data["kernels"][kernel_id] = signal
        data["signals"].append({"id": kernel_id, "signal": signal, "t": time.time()})
        data["signals"] = data["signals"][-300:]
        self.write(data)


# =========================
# 🧠 V42 KERNEL FEDERATION NODE
# =========================
class OmegaKernelV42:
    def __init__(self):
        self.state = OmegaState()
        self.identity = IdentityCore()
        self.bus = KernelBus()

        self.kernel_id = f"kernel_{random.randint(1000,9999)}"

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.memory = deque(maxlen=200)

        self.tick_rate = 1

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate(self):
        return {n: random.random() for n in self.nodes}

    # -------------------------
    # CROSS-KERNEL INFLUENCE
    # -------------------------
    def ingest_federation(self):
        bus = self.bus.read()

        signals = bus.get("kernels", {})

        if not signals:
            return 1.0

        return sum(signals.values()) / (len(signals) + 1e-9)

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate()

        federation_signal = self.ingest_federation()

        # weighted decision
        selected = max(signals.items(), key=lambda x: x[1] * federation_signal)

        node, strength = selected

        self.memory.append(node)

        # identity update (stabilization core)
        self.identity.update(self.kernel_id, strength)

        # publish to global bus
        self.bus.publish(self.kernel_id, strength)

        self.state.remember({
            "tick": tick,
            "selected": node,
            "strength": strength,
            "federation": federation_signal,
            "identity_stability": self.identity.state["stability"]
        })

        print(
            f"[V42] tick={tick} | "
            f"id={self.kernel_id} | "
            f"active={node} | "
            f"fed={federation_signal:.3f} | "
            f"stable={self.identity.state['stability']:.3f}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V42] IDENTITY STABILIZATION + KERNEL FEDERATION ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV42().run()
