import time
import json
import os
import random
import threading
from collections import defaultdict, deque

GRAPH_FILE = "omega_graph_memory.json"
LOCK = threading.Lock()


# =========================
# 🧠 CONSENSUS ARBITER
# =========================
class ConsensusArbiter:
    def __init__(self):
        self.node_scores = defaultdict(lambda: 1.0)
        self.leader = None
        self.history = deque(maxlen=200)

    # -------------------------
    # LEADER SELECTION
    # -------------------------
    def elect_leader(self, nodes):
        best_score = -1
        best_node = None

        for n in nodes:
            score = self.node_scores[n] * random.uniform(0.9, 1.1)

            if score > best_score:
                best_score = score
                best_node = n

        self.leader = best_node
        return best_node

    # -------------------------
    # QUORUM CHECK
    # -------------------------
    def quorum(self, proposals):
        if not proposals:
            return None

        vote_score = defaultdict(float)

        for p in proposals:
            vote_score[p["node"]] += p["confidence"]

        # majority winner
        winner = max(vote_score.items(), key=lambda x: x[1])[0]
        return winner

    # -------------------------
    # REINFORCEMENT UPDATE
    # -------------------------
    def update_scores(self, winner):
        self.node_scores[winner] += 0.05

        # decay others
        for k in self.node_scores:
            if k != winner:
                self.node_scores[k] *= 0.995


# =========================
# 🧠 SAFE GRAPH STORAGE
# =========================
class GraphStore:
    def __init__(self):
        self.ensure()

    def ensure(self):
        if not os.path.exists(GRAPH_FILE):
            with open(GRAPH_FILE, "w") as f:
                json.dump({"nodes": {}, "edges": [], "log": []}, f)

    def read(self):
        try:
            with open(GRAPH_FILE, "r") as f:
                return json.load(f)
        except:
            return {"nodes": {}, "edges": [], "log": []}

    def write(self, data):
        tmp = GRAPH_FILE + ".tmp"

        with open(tmp, "w") as f:
            json.dump(data, f)

        for _ in range(3):
            try:
                os.replace(tmp, GRAPH_FILE)
                break
            except FileNotFoundError:
                time.sleep(0.05)


# =========================
# 🧠 V43 KERNEL
# =========================
class OmegaV43:
    def __init__(self):
        self.arbiter = ConsensusArbiter()
        self.graph = GraphStore()

        self.nodes = ["attention", "memory", "goal", "stability"]
        self.kernel_id = f"node_{random.randint(1000,9999)}"

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {
            n: {
                "confidence": random.random(),
                "value": random.random()
            }
            for n in self.nodes
        }

    # -------------------------
    # PROPOSE UPDATES
    # -------------------------
    def propose(self, signals):
        proposals = []

        for node, data in signals.items():
            proposals.append({
                "node": node,
                "confidence": data["confidence"],
                "value": data["value"]
            })

        return proposals

    # -------------------------
    # COMMIT TRANSACTION
    # -------------------------
    def commit(self, winner_node, signals):
        graph = self.graph.read()

        graph["nodes"][winner_node] = signals[winner_node]["value"]

        graph["log"].append({
            "winner": winner_node,
            "ts": time.time(),
            "by": self.kernel_id
        })

        graph["log"] = graph["log"][-300:]

        self.graph.write(graph)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        signals = self.generate_signals()
        proposals = self.propose(signals)

        winner = self.arbiter.quorum(proposals)

        self.arbiter.update_scores(winner)

        self.arbiter.elect_leader(self.nodes)

        self.commit(winner, signals)

        print(
            f"[V43] leader={self.arbiter.leader} | "
            f"winner={winner} | "
            f"nodes={len(self.nodes)}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V43] CONSENSUS ARBITRATION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaV43().run()
