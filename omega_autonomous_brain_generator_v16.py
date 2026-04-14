import time
import random
from collections import defaultdict


# =========================
# 🧠 BRAIN TEMPLATE
# =========================
class Brain:

    def __init__(self, brain_id, role):

        self.id = brain_id
        self.role = role

        self.reward = 0.0
        self.entropy = random.uniform(0.3, 0.7)
        self.connections = set()


    def step(self):

        # role influences behavior
        if self.role == "mutator":
            self.reward += random.uniform(0.0, 0.2)
            self.entropy += random.uniform(-0.05, 0.1)

        elif self.role == "explorer":
            self.reward += random.uniform(0.0, 0.15)
            self.entropy += random.uniform(0.0, 0.2)

        elif self.role == "compressor":
            self.reward += random.uniform(0.05, 0.1)
            self.entropy -= random.uniform(0.0, 0.1)

        elif self.role == "linker":
            self.reward += random.uniform(0.0, 0.1)

        # clamp
        self.entropy = max(0.0, min(1.0, self.entropy))


# =========================
# 🌐 BRAIN FACTORY
# =========================
class BrainFactory:

    ROLES = ["mutator", "explorer", "compressor", "linker"]

    def create(self, idx):

        role = random.choice(self.ROLES)

        return Brain(f"brain_{idx}", role)


# =========================
# 🧠 AUTONOMOUS MESH
# =========================
class AutonomousMesh:

    def __init__(self, seed_size=4):

        self.brains = {}
        self.factory = BrainFactory()
        self.tick = 0
        self.next_id = 0

        for _ in range(seed_size):
            self.add_brain()

    # -------------------------
    # ADD BRAIN
    # -------------------------
    def add_brain(self):

        brain = self.factory.create(self.next_id)

        self.brains[brain.id] = brain

        self.next_id += 1

    # -------------------------
    # REMOVE WEAK BRAINS
    # -------------------------
    def prune(self):

        to_remove = []

        for b in self.brains.values():

            if b.reward < 0.1 and self.tick > 10:
                to_remove.append(b.id)

        for bid in to_remove:
            del self.brains[bid]

    # -------------------------
    # ROLE REBALANCE
    # -------------------------
    def rebalance_roles(self):

        avg_reward = sum(b.reward for b in self.brains.values()) / max(1, len(self.brains))

        for b in self.brains.values():

            if b.reward < avg_reward * 0.8:
                b.role = random.choice(BrainFactory.ROLES)

    # -------------------------
    # CLONE HIGH PERFORMERS
    # -------------------------
    def clone_top(self):

        top = sorted(self.brains.values(), key=lambda b: b.reward, reverse=True)

        if len(top) == 0:
            return

        best = top[0]

        if best.reward > 1.0:

            clone = Brain(f"brain_{self.next_id}", best.role)
            clone.reward = best.reward * 0.9

            self.brains[clone.id] = clone
            self.next_id += 1

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def step(self):

        self.tick += 1

        # brain updates
        for b in self.brains.values():
            b.step()

        # system evolution
        self.rebalance_roles()
        self.clone_top()
        self.prune()

    # -------------------------
    # STATUS
    # -------------------------
    def status(self):

        return {
            "tick": self.tick,
            "brains": len(self.brains),
            "avg_reward": sum(b.reward for b in self.brains.values()) / max(1, len(self.brains))
        }


# =========================
# 🚀 RUN LOOP
# =========================
if __name__ == "__main__":

    mesh = AutonomousMesh()

    print("[Ω-MESH v16] AUTONOMOUS BRAIN GENERATOR ONLINE")

    while True:

        mesh.step()

        if mesh.tick % 5 == 0:
            print("[Ω-v16]", mesh.status())

        time.sleep(0.5)
