import time
import random
import threading
from collections import defaultdict, deque

# =========================
# OMEGA MESH KERNEL V5
# Autonomous Cognition Emergence
# =========================

# -------------------------
# IDEA OBJECT (SELF-REPLICATING)
# -------------------------
class Idea:
    def __init__(self, content, strength, origin):
        self.content = content
        self.strength = strength
        self.origin = origin
        self.age = 0
        self.alive = True

    # IDEA GENERATES IDEAS
    def spawn(self):
        if self.strength < 0.2:
            return None

        return Idea(
            content=self.content + "_child",
            strength=self.strength * random.uniform(0.6, 1.1),
            origin=self.origin
        )

    def mutate(self):
        self.strength += random.uniform(-0.05, 0.05)
        self.strength = max(0, min(1, self.strength))
        self.age += 1

        if self.strength < 0.05:
            self.alive = False


# -------------------------
# ADAPTIVE NODE (DYNAMIC ROLE)
# -------------------------
class OmegaNode:
    def __init__(self, node_id):
        self.id = node_id

        self.memory = deque(maxlen=500)
        self.ideas = []

        self.reputation = 1.0
        self.coherence = 0.5

        self.role = "neutral"

    # -------------------------
    # ROLE EVOLUTION
    # -------------------------
    def adapt_role(self):
        if self.reputation > 1.5:
            self.role = "thinker"
        elif self.coherence > 0.7:
            self.role = "watcher"
        elif len(self.ideas) > 50:
            self.role = "worker"
        else:
            self.role = "neutral"

    # -------------------------
    # RECEIVE IDEA
    # -------------------------
    def receive(self, idea):
        self.memory.append(idea.content)
        self.ideas.append(idea)

        if self.role == "thinker":
            self.coherence += 0.02
        elif self.role == "worker":
            idea.strength += 0.03
        elif self.role == "watcher":
            self.reputation += 0.01

    # -------------------------
    # NODE THINKING
    # -------------------------
    def think(self):
        if self.role != "thinker":
            return None

        return Idea(
            content=f"thought_{random.randint(1,9999)}",
            strength=random.random(),
            origin=self.id
        )

    # -------------------------
    # UPDATE METRICS
    # -------------------------
    def update(self):
        alive = sum(1 for i in self.ideas if i.alive)
        self.reputation = (alive / (len(self.ideas) + 1)) + self.coherence
        self.adapt_role()


# -------------------------
# GLOBAL COGNITION FIELD
# -------------------------
class CognitiveField:
    def __init__(self):
        self.field = deque(maxlen=1000)

    def write(self, idea):
        self.field.append(idea)

    def read_all(self):
        return list(self.field)


# -------------------------
# OMEGA SWARM BRAIN
# -------------------------
class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}
        self.field = CognitiveField()

        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "emergence": 0.0
        }

    # -------------------------
    # REGISTER NODE
    # -------------------------
    def register(self, node_id):
        self.nodes[node_id] = OmegaNode(node_id)
        print(f"[OMEGA] Node active: {node_id}")

    # -------------------------
    # PROPAGATE FIELD
    # -------------------------
    def propagate(self, idea):
        self.field.write(idea)

        for node in self.nodes.values():
            node.receive(idea)

    # -------------------------
    # EMERGENT LOOP
    # -------------------------
    def heartbeat(self):
        while True:
            self.state["tick"] += 1

            new_ideas = []

            # NODE THINKING
            for node in self.nodes.values():
                node.update()

                idea = node.think()
                if idea:
                    new_ideas.append(idea)

            # IDEA GENERATION + SELF-REPLICATION
            for idea in list(self.field.read_all()):
                child = idea.spawn()
                if child:
                    new_ideas.append(child)

            # PROPAGATION
            for idea in new_ideas:
                self.propagate(idea)

            # MUTATION LOOP
            for idea in self.field.field:
                idea.mutate()

            # ENTROPY
            alive = sum(1 for i in self.field.field if i.alive)
            total = len(self.field.field) + 1
            self.state["entropy"] = 1 - (alive / total)

            # EMERGENCE = complexity growth
            self.state["emergence"] = len(self.field.field) * sum(
                n.reputation for n in self.nodes.values()
            ) / (len(self.nodes) + 1)

            time.sleep(1)

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.state["tick"],
            "entropy": round(self.state["entropy"], 4),
            "emergence": round(self.state["emergence"], 4),
            "nodes": len(self.nodes),
            "ideas": len(self.field.field)
        }


# =========================
# DEMO
# =========================
if __name__ == "__main__":
    swarm = OmegaSwarmBus()

    swarm.register("A")
    swarm.register("B")
    swarm.register("C")
    swarm.register("D")

    threading.Thread(target=swarm.heartbeat, daemon=True).start()

    while True:
        time.sleep(2)
        print("[OMEGA V5]", swarm.snapshot())
