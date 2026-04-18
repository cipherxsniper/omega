import random
import math

# 🧠 OMEGA v16 — SWARM COGNITION MESH

class SwarmNode:

    def __init__(self, name):
        self.name = name

        self.state = random.uniform(0.3, 0.7)
        self.energy = 0.5
        self.fitness = 0.5

        # directed weighted connections
        self.links = {}

        # leadership metrics
        self.influence = 0.0
        self.leadership_score = 0.0

    # -------------------------
    # CONNECTION MECHANISM
    # -------------------------
    def connect(self, other):
        self.links[other.name] = random.uniform(0.1, 0.5)

    # -------------------------
    # SEND SIGNAL (limited bandwidth)
    # -------------------------
    def emit(self, swarm):
        signals = []

        # top-K strongest connections only (bandwidth constraint)
        top_links = sorted(self.links.items(), key=lambda x: x[1], reverse=True)[:3]

        for target_name, weight in top_links:
            target = swarm.get(target_name)
            if target:
                signal = self.state * weight
                signals.append((target, signal))

        return signals

    # -------------------------
    # RECEIVE SIGNAL
    # -------------------------
    def receive(self, signal):
        self.state += signal * 0.1
        self.state = max(0.01, min(1.0, self.state))

    # -------------------------
    # UPDATE DYNAMICS
    # -------------------------
    def update(self):
        self.energy += (self.state - 0.5) * 0.05
        self.fitness = (self.energy * 0.6) + (self.state * 0.4)

    # -------------------------
    # LEADERSHIP CALCULATION
    # -------------------------
    def compute_leadership(self):
        self.leadership_score = (
            self.fitness * 0.5 +
            len(self.links) * 0.1 +
            self.energy * 0.4
        )


# =========================
# 🧠 SWARM MESH ENGINE
# =========================

class SwarmMesh:

    def __init__(self):
        self.nodes = {}
        self.leaders = []

    def add(self, node):
        self.nodes[node.name] = node

    def get(self, name):
        return self.nodes.get(name)

    # -------------------------
    # LEADERSHIP SELECTION
    # -------------------------
    def update_leaders(self):

        for n in self.nodes.values():
            n.compute_leadership()

        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda x: x.leadership_score,
            reverse=True
        )

        # top 20% become leaders
        cutoff = max(1, len(sorted_nodes) // 5)
        self.leaders = sorted_nodes[:cutoff]

    # -------------------------
    # HIERARCHICAL FLOW
    # -------------------------
    def propagate(self):

        messages = []

        # leaders amplify influence
        for leader in self.leaders:
            leader.state += 0.05  # dominance boost

        for node in self.nodes.values():
            messages.extend(node.emit(self.nodes))

        for target, signal in messages:
            target.receive(signal)

    # -------------------------
    # SWARM EVOLUTION STEP
    # -------------------------
    def step(self):

        self.update_leaders()
        self.propagate()

        for n in self.nodes.values():
            n.update()

        return {
            n.name: {
                "state": n.state,
                "fitness": n.fitness,
                "leader": n in self.leaders
            }
            for n in self.nodes.values()
        }


# =========================
# 🧪 BOOTSTRAP
# =========================

if __name__ == "__main__":

    swarm = SwarmMesh()

    for i in range(8):
        swarm.add(SwarmNode(f"node_{i}"))

    # random connections
    for n in swarm.nodes.values():
        for m in swarm.nodes.values():
            if n != m:
                n.connect(m)

    for step in range(10):
        print("\nSTEP:", step)
        print(swarm.step())
