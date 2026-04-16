import time
import json
import math
import threading
from collections import defaultdict, deque

# ==============================
# 🧠 MEMORY CORE
# ==============================
class MemoryCore:
    def __init__(self, max_stm=200):
        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(int)
        self.patterns = defaultdict(int)
        self.anomalies = []
        self.tick = 0
        self.last_state = None

    def compress(self, state):
        e = round(state.get("entropy", 0), 2)
        s = round(state.get("stability", 0), 2)
        n = int(state.get("nodes", 0) / 5) * 5
        return f"E{e}_S{s}_N{n}"

    def ingest(self, state):
        self.stm.append(state)
        self.tick += 1

        sig = self.compress(state)
        self.patterns[sig] += 1

        if self.last_state:
            de = abs(state["entropy"] - self.last_state["entropy"])
            ds = abs(state["stability"] - self.last_state["stability"])

            if de > 0.5 or ds > 0.5:
                self.anomalies.append((self.tick, state))

        self.last_state = state

        if self.tick % 10 == 0:
            self.consolidate()

    def consolidate(self):
        for s in list(self.stm):
            self.ltm[self.compress(s)] += 1

# ==============================
# 🌐 MESH BUS
# ==============================
class MeshBus:
    def __init__(self):
        self.nodes = {}
        self.messages = deque(maxlen=500)

    def register(self, node):
        self.nodes[node.node_id] = node

    def broadcast(self, sender_id, payload):
        msg = {
            "from": sender_id,
            "payload": payload,
            "time": time.time()
        }
        self.messages.append(msg)

        for nid, node in self.nodes.items():
            if nid != sender_id:
                node.receive(msg)

# ==============================
# 🧩 NODE
# ==============================
class OmegaNode:
    def __init__(self, node_id, bus: MeshBus):
        self.node_id = node_id
        self.bus = bus
        self.memory = MemoryCore()
        self.inbox = deque(maxlen=100)

        self.bus.register(self)

    def generate_state(self):
        t = self.memory.tick + 1
        return {
            "entropy": math.sin(t / 5) + math.cos(t / 7),
            "stability": math.cos(t / 9),
            "nodes": len(self.bus.nodes)
        }

    def step(self):
        state = self.generate_state()
        self.memory.ingest(state)

        signal = {
            "sig": self.memory.compress(state),
            "patterns": len(self.memory.patterns),
            "anomalies": len(self.memory.anomalies)
        }

        self.bus.broadcast(self.node_id, signal)

    def receive(self, msg):
        self.inbox.append(msg)

# ==============================
# 🧰 WATCHDOG
# ==============================
class Watchdog(threading.Thread):
    def __init__(self, bus: MeshBus):
        super().__init__()
        self.bus = bus
        self.running = True

    def run(self):
        while self.running:
            if len(self.bus.messages) > 400:
                print("[WATCHDOG] High mesh load detected")
            time.sleep(1)

# ==============================
# 🧠 SWARM ENGINE
# ==============================
class OmegaSwarm:
    def __init__(self, node_count=5):
        self.bus = MeshBus()
        self.nodes = [OmegaNode(f"node_{i}", self.bus) for i in range(node_count)]
        self.watchdog = Watchdog(self.bus)

    def run(self, steps=50):
        self.watchdog.start()

        for i in range(steps):
            for n in self.nodes:
                n.step()

            if i % 10 == 0:
                self.print_state()

            time.sleep(0.2)

        self.watchdog.running = False

    def print_state(self):
        total_patterns = sum(len(n.memory.patterns) for n in self.nodes)
        total_anomalies = sum(len(n.memory.anomalies) for n in self.nodes)

        print({
            "nodes": len(self.nodes),
            "patterns": total_patterns,
            "anomalies": total_anomalies,
            "messages": len(self.bus.messages)
        })

# ==============================
# 🚀 RUN
# ==============================
if __name__ == "__main__":
    swarm = OmegaSwarm(node_count=5)
    swarm.run(steps=30)
