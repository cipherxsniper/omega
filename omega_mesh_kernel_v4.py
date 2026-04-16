import time
import random
import threading
from collections import defaultdict, deque

# =========================
# OMEGA MESH KERNEL V4
# Cognition Mesh Upgrade
# =========================

# -------------------------
# NODE ROLES
# -------------------------
THINKER = "thinker"
WORKER = "worker"
WATCHER = "watcher"
ARCHIVIST = "archivist"


class Idea:
    def __init__(self, content, strength, origin):
        self.content = content
        self.strength = strength
        self.origin = origin
        self.age = 0
        self.alive = True

    def mutate(self):
        # slight drift over time
        self.strength += random.uniform(-0.05, 0.05)
        self.strength = max(0, min(1, self.strength))
        self.age += 1

        if self.strength < 0.1:
            self.alive = False


class OmegaNode:
    def __init__(self, node_id, role):
        self.id = node_id
        self.role = role

        self.memory = deque(maxlen=300)
        self.ideas = []
        self.reputation = 1.0
        self.coherence = 0.5

        self.success_rate = 0.5

    # -------------------------
    # RECEIVE IDEA
    # -------------------------
    def receive(self, idea):
        self.memory.append(idea.content)
        self.ideas.append(idea)

        # role-based reaction
        if self.role == WATCHER:
            self.coherence += 0.02
        elif self.role == THINKER:
            idea.strength += 0.05
        elif self.role == WORKER:
            idea.strength += random.uniform(-0.02, 0.08)
        elif self.role == ARCHIVIST:
            self.reputation += 0.01

    # -------------------------
    # GENERATE IDEA
    # -------------------------
    def generate(self):
        if self.role != THINKER:
            return None

        return Idea(
            content=f"idea_{random.randint(1,999)}",
            strength=random.random(),
            origin=self.id
        )

    # -------------------------
    # UPDATE REPUTATION
    # -------------------------
    def update(self):
        alive_ideas = sum(1 for i in self.ideas if i.alive)
        self.success_rate = alive_ideas / (len(self.ideas) + 1)

        self.reputation = (
            0.5 * self.success_rate +
            0.5 * self.coherence
        )


class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}
        self.global_ideas = deque(maxlen=500)

        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "consensus": 1.0
        }

    # -------------------------
    # REGISTER NODE
    # -------------------------
    def register(self, node_id, role):
        self.nodes[node_id] = OmegaNode(node_id, role)
        print(f"[OMEGA] {node_id} -> {role}")

    # -------------------------
    # IDEA BROADCAST
    # -------------------------
    def broadcast_idea(self, idea):
        for node in self.nodes.values():
            node.receive(idea)

    # -------------------------
    # CONFLICT RESOLUTION
    # -------------------------
    def resolve(self):
        if not self.global_ideas:
            return

        best = max(
            self.global_ideas,
            key=lambda i: i.strength
        )

        # weak ideas decay
        for idea in self.global_ideas:
            if idea.strength < best.strength * 0.4:
                idea.alive = False

    # -------------------------
    # SWARM COGNITION LOOP
    # -------------------------
    def heartbeat(self):
        while True:
            self.state["tick"] += 1

            new_ideas = []

            # node thinking phase
            for node in self.nodes.values():
                node.update()

                idea = node.generate()
                if idea:
                    new_ideas.append(idea)

            # idea propagation
            for idea in new_ideas:
                self.global_ideas.append(idea)
                self.broadcast_idea(idea)

            # mutate ideas
            for idea in list(self.global_ideas):
                idea.mutate()

            # resolve conflicts
            self.resolve()

            # entropy update
            alive = sum(1 for i in self.global_ideas if i.alive)
            self.state["entropy"] = 1 - (alive / (len(self.global_ideas) + 1))

            # consensus emerges from reputation
            rep = sum(n.reputation for n in self.nodes.values())
            self.state["consensus"] = rep / (len(self.nodes) + 1)

            time.sleep(1)

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.state["tick"],
            "entropy": round(self.state["entropy"], 4),
            "consensus": round(self.state["consensus"], 4),
            "ideas": len(self.global_ideas),
            "alive": sum(1 for i in self.global_ideas if i.alive)
        }


# =========================
# DEMO
# =========================
if __name__ == "__main__":
    swarm = OmegaSwarmBus()

    swarm.register("A", THINKER)
    swarm.register("B", WORKER)
    swarm.register("C", WATCHER)
    swarm.register("D", ARCHIVIST)

    threading.Thread(target=swarm.heartbeat, daemon=True).start()

    while True:
        time.sleep(2)
        print("[OMEGA V4]", swarm.snapshot())
