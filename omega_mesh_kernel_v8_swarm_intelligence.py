import time
import math
import threading
from collections import defaultdict, deque

# ==============================
# 🧠 SHARED SWARM BRAIN
# ==============================
class SwarmBrain:
    def __init__(self):
        self.global_beliefs = defaultdict(float)
        self.confidence = defaultdict(float)

    def update(self, pattern, weight=1.0):
        self.global_beliefs[pattern] += weight
        self.confidence[pattern] = self.global_beliefs[pattern] / (self.global_beliefs[pattern] + 1)

    def consensus_score(self, pattern):
        return self.confidence.get(pattern, 0.0)

# ==============================
# 🧠 MEMORY CORE (ENHANCED)
# ==============================
class MemoryCore:
    def __init__(self):
        self.stm = deque(maxlen=200)
        self.patterns = defaultdict(int)
        self.last_state = None

    def compress(self, state):
        e = round(state["entropy"], 2)
        s = round(state["stability"], 2)
        return f"E{e}_S{s}"

    def ingest(self, state, swarm_brain: SwarmBrain):
        self.stm.append(state)

        sig = self.compress(state)
        self.patterns[sig] += 1

        # push into swarm brain
        swarm_brain.update(sig)

        self.last_state = state

# ==============================
# 🧩 NODE (SWARM-AWARE)
# ==============================
class OmegaNode:
    def __init__(self, node_id, swarm_brain: SwarmBrain):
        self.node_id = node_id
        self.memory = MemoryCore()
        self.swarm = swarm_brain
        self.inbox = deque(maxlen=100)
        self.bias = 1.0

    def generate_state(self):
        t = len(self.memory.stm) + 1
        return {
            "entropy": math.sin(t / 4) + math.cos(t / 6),
            "stability": math.cos(t / 8)
        }

    def swarm_adjustment(self, pattern):
        consensus = self.swarm.consensus_score(pattern)

        # adjust bias based on swarm agreement
        if consensus > 0.7:
            self.bias *= 1.01
        elif consensus < 0.3:
            self.bias *= 0.99

    def step(self):
        state = self.generate_state()
        sig = self.memory.compress(state)

        self.memory.ingest(state, self.swarm)
        self.swarm_adjustment(sig)

    def receive(self, msg):
        self.inbox.append(msg)

# ==============================
# 🌐 SWARM ENGINE
# ==============================
class OmegaSwarmV8:
    def __init__(self, n=5):
        self.swarm_brain = SwarmBrain()
        self.nodes = [OmegaNode(f"node_{i}", self.swarm_brain) for i in range(n)]
        self.tick = 0

    def run(self, steps=50):
        for _ in range(steps):
            self.tick += 1

            for node in self.nodes:
                node.step()

            if self.tick % 10 == 0:
                self.report()

            time.sleep(0.1)

    def report(self):
        top = sorted(
            self.swarm_brain.global_beliefs.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        avg_bias = sum(n.bias for n in self.nodes) / len(self.nodes)

        print({
            "tick": self.tick,
            "top_beliefs": top,
            "avg_bias": round(avg_bias, 4)
        })

# ==============================
# 🚀 RUN
# ==============================
if __name__ == "__main__":
    swarm = OmegaSwarmV8(n=5)
    swarm.run(steps=60)
