import time
import uuid
import random
from collections import defaultdict, deque


# =========================================================
# 🌐 MESSAGE BUS (NERVOUS SYSTEM)
# =========================================================
class OmegaBus:
    def __init__(self):
        self.messages = deque(maxlen=500)

    def emit(self, msg):
        msg["id"] = str(uuid.uuid4())[:8]
        msg["timestamp"] = time.time()
        self.messages.append(msg)

    def broadcast(self):
        return list(self.messages)


# =========================================================
# 🧠 BASE NODE (NEURON)
# =========================================================
class OmegaNode:
    def __init__(self, node_id, role, bus):
        self.node_id = node_id
        self.role = role
        self.bus = bus

        self.memory = defaultdict(float)
        self.tick = 0
        self.energy = 1.0

    def process(self, input_state):
        self.tick += 1

        output = self._compute(input_state)
        self._learn(input_state)

        self.bus.emit({
            "from": self.node_id,
            "role": self.role,
            "type": "signal",
            "payload": output
        })

        return output

    def _compute(self, state):
        # base cognition transform
        return {
            "node": self.node_id,
            "role": self.role,
            "entropy_shift": state["entropy"] * random.uniform(0.9, 1.1),
            "stability_shift": state["stability"] * random.uniform(0.9, 1.1)
        }

    def _learn(self, state):
        self.memory["entropy"] += state["entropy"] * 0.01
        self.memory["stability"] += state["stability"] * 0.01


# =========================================================
# 🛡 WATCHDOG NODE (STABILITY CONTROL)
# =========================================================
class WatchdogNode(OmegaNode):
    def _compute(self, state):
        anomaly = abs(state["entropy"]) > 1.2 or abs(state["stability"]) > 1.2

        return {
            "node": self.node_id,
            "role": "watchdog",
            "anomaly": anomaly,
            "risk_score": abs(state["entropy"]) + abs(state["stability"])
        }


# =========================================================
# 🧠 CREATIVE NODE
# =========================================================
class CreativeNode(OmegaNode):
    def _compute(self, state):
        return {
            "node": self.node_id,
            "role": "creative",
            "idea_seed": state["entropy"] + state["stability"] + random.random(),
            "novelty": random.random()
        }


# =========================================================
# 🧠 OMEGA KERNEL CORE
# =========================================================
class OmegaMeshKernelV1:
    def __init__(self):
        self.bus = OmegaBus()

        self.nodes = [
            OmegaNode("cog-1", "cognition", self.bus),
            CreativeNode("cre-1", "creative", self.bus),
            WatchdogNode("wd-1", "watchdog", self.bus),
        ]

        self.global_memory = defaultdict(float)
        self.tick = 0

    def ingest(self, state):
        self.tick += 1

        results = []
        for node in self.nodes:
            result = node.process(state)
            results.append(result)

            # global memory accumulation
            for k, v in result.items():
                if isinstance(v, (int, float)):
                    self.global_memory[k] += v * 0.01

        return {
            "tick": self.tick,
            "results": results,
            "memory_size": len(self.global_memory)
        }

    def snapshot(self):
        return {
            "tick": self.tick,
            "global_memory": dict(self.global_memory),
            "bus_size": len(self.bus.messages)
        }


# =========================================================
# 🚀 DEMO RUN
# =========================================================
if __name__ == "__main__":
    kernel = OmegaMeshKernelV1()

    for i in range(20):
        state = {
            "entropy": random.uniform(-1, 1),
            "stability": random.uniform(-1, 1)
        }

        out = kernel.ingest(state)
        print(out["tick"], out["memory_size"])

    print("\nFINAL SNAPSHOT")
    print(kernel.snapshot())
