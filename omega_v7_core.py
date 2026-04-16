import random
import time

class OmegaV7:
    def __init__(self):
        self.nodes = ["brain", "system", "observer", "executor"]

        self.state = {
            "AWARE": True,
            "entropy": 0.5,
            "learning_rate": 0.05
        }

        self.memory = []
        self.node_scores = {n: 0.5 for n in self.nodes}
        self.node_history = {n: [] for n in self.nodes}

        self.policy = {
            "attention": {n: 0.25 for n in self.nodes}
        }

    # === COMMUNICATION BUS ===
    def broadcast(self, message):
        for node in self.nodes:
            self.receive(node, message)

    def receive(self, node, message):
        self.node_history[node].append(message)

    # === LEARNING ===
    def learn(self, node, success):
        delta = self.state["learning_rate"]

        if success:
            self.node_scores[node] += delta
        else:
            self.node_scores[node] -= delta

        self.node_scores[node] = max(0, min(1, self.node_scores[node]))

    # === META LEARNING ===
    def adapt_learning_rate(self):
        avg = sum(self.node_scores.values()) / len(self.node_scores)

        if avg > 0.6:
            self.state["learning_rate"] *= 0.98
        else:
            self.state["learning_rate"] *= 1.02

        self.state["learning_rate"] = max(0.01, min(0.1, self.state["learning_rate"]))

    # === EVOLUTION ENGINE ===
    def evolve(self):
        # mutate attention weights slightly
        for n in self.policy["attention"]:
            self.policy["attention"][n] *= random.uniform(0.95, 1.05)

        self.normalize_attention()

    def normalize_attention(self):
        total = sum(self.policy["attention"].values())
        for n in self.policy["attention"]:
            self.policy["attention"][n] /= total

    # === NODE SELECTION ===
    def choose_node(self):
        r = random.random()
        cumulative = 0

        for node, weight in self.policy["attention"].items():
            cumulative += weight
            if r <= cumulative:
                return node

        return self.nodes[0]

    # === ENVIRONMENT SCANNER (SAFE) ===
    def scan_environment(self):
        # controlled simulated external input
        signals = ["stable", "noise", "opportunity", "risk"]
        return random.choice(signals)

    # === POLICY GOVERNOR ===
    def regulate(self):
        if self.state["entropy"] > 0.85:
            for n in self.policy["attention"]:
                self.policy["attention"][n] *= 0.9

        self.normalize_attention()

    # === MAIN LOOP ===
    def step(self, tick):
        env = self.scan_environment()

        node = self.choose_node()

        # simulate outcome
        success = random.random() > self.state["entropy"]

        self.learn(node, success)
        self.adapt_learning_rate()
        self.evolve()
        self.regulate()

        # update entropy
        if success:
            self.state["entropy"] *= 0.98
        else:
            self.state["entropy"] *= 1.02

        self.state["entropy"] = min(self.state["entropy"], 0.9)

        # communication
        self.broadcast({
            "tick": tick,
            "node": node,
            "env": env,
            "success": success
        })

        return {
            "tick": tick,
            "node": node,
            "success": success,
            "entropy": self.state["entropy"],
            "learning_rate": self.state["learning_rate"],
            "scores": self.node_scores,
            "aware": self.state["AWARE"]
        }
