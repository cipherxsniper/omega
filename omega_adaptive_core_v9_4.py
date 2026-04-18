# 🧠 OMEGA v9.4 - FEEDBACK LEARNING ENGINE (CONTROLLED EVOLUTION)
# ---------------------------------------------------------------
# Multi-directory scanning + adaptive node behavior + learning loop
# SAFE: no uncontrolled file creation, no self-replication
# ---------------------------------------------------------------

import os
import ast
import time
from collections import defaultdict


# ----------------------------
# CONFIG
# ----------------------------
SCAN_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]


# ----------------------------
# NODE GRAPH BUILDER
# ----------------------------
class NodeGraphV9_4:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def scan_file(self, filepath):

        try:
            with open(filepath, "r") as f:
                tree = ast.parse(f.read(), filename=filepath)

            node_name = os.path.basename(filepath)

            self.nodes.add(node_name)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        self.edges[node_name].add(n.name)

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.edges[node_name].add(node.module)

        except:
            pass

    def scan_directory(self, path):

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    self.scan_file(os.path.join(root, file))


# ----------------------------
# EVENT MEMORY (LEARNING CORE)
# ----------------------------
class EventMemoryV9_4:

    def __init__(self):
        self.memory = defaultdict(list)

    def record(self, node, score, reward):

        self.memory[node].append({
            "score": score,
            "reward": reward,
            "t": time.time()
        })

    def trend(self, node):

        data = self.memory[node]

        if len(data) < 3:
            return 0.0

        recent = [d["reward"] for d in data[-10:]]

        return sum(recent) / len(recent)


# ----------------------------
# ADAPTIVE DECISION ENGINE
# ----------------------------
class AdaptiveDecisionV9_4:

    def decide(self, node, score, trend):

        # learning bias
        adjusted = score + (trend * 0.3)

        if adjusted > 0.75:
            return "OPTIMIZE"

        if adjusted < 0.4:
            return "RESTRUCTURE"

        return "NO_ACTION"


# ----------------------------
# SIMULATED NODE COMMUNICATION BUS
# ----------------------------
class VirtualBus:

    def __init__(self):
        self.messages = []

    def send(self, sender, receiver, payload):
        self.messages.append((sender, receiver, payload))

    def read(self):
        return self.messages[-50:]


# ----------------------------
# ORCHESTRATOR
# ----------------------------
class OmegaAdaptiveCoreV9_4:

    def __init__(self):

        self.graph = NodeGraphV9_4()
        self.memory = EventMemoryV9_4()
        self.decision = AdaptiveDecisionV9_4()
        self.bus = VirtualBus()

        self.node_state = {}

    def scan_all(self):

        print("🧠 SCANNING OMEGA ECOSYSTEM...")

        for path in SCAN_PATHS:
            if os.path.exists(path):
                self.graph.scan_directory(path)

        print(f"✔ Nodes: {len(self.graph.nodes)}")
        print(f"✔ Edges: {len(self.graph.edges)}")

    def cycle(self):

        for node in list(self.graph.nodes)[:10]:

            score = 0.5  # placeholder dynamic signal

            trend = self.memory.trend(node)

            decision = self.decision.decide(node, score, trend)

            reward = 0.1 if decision == "OPTIMIZE" else 0.0

            self.memory.record(node, score, reward)

            self.bus.send(node, "system", {
                "decision": decision,
                "score": score,
                "trend": trend
            })

            self.node_state[node] = decision

            print(f"[{node}] {decision} | trend={trend:.2f}")

    def run(self):

        self.scan_all()

        print("🧠 OMEGA v9.4 ADAPTIVE CORE ONLINE")

        while True:
            self.cycle()
            time.sleep(2)


if __name__ == "__main__":
    OmegaAdaptiveCoreV9_4().run()
