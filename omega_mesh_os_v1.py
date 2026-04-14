import random
import time
from collections import defaultdict


# =========================================================
# 🧠 COGNITIVE CELL (OPTION 1)
# =========================================================
class CognitiveCell:
    def __init__(self, cell_id):
        self.id = cell_id
        self.energy = random.uniform(0.8, 1.2)
        self.coherence = random.uniform(0.4, 0.6)
        self.memory = []

    def think(self, input_signal):
        noise = random.uniform(-0.03, 0.03)

        self.coherence += input_signal * 0.02 + noise
        self.coherence = max(0.0, min(1.0, self.coherence))

        self.energy += (self.coherence - 0.5) * 0.01

        self.memory.append(self.coherence)

        if len(self.memory) > 50:
            self.memory.pop(0)

        return self.coherence


# =========================================================
# 🧠 MESH NETWORK (OPTION 2)
# =========================================================
class CognitiveMesh:
    def __init__(self, size=5):
        self.cells = [CognitiveCell(i) for i in range(size)]
        self.signal_bus = defaultdict(float)

    def broadcast(self):
        avg = sum(c.coherence for c in self.cells) / len(self.cells)
        for i in range(len(self.cells)):
            self.signal_bus[i] += (avg - self.cells[i].coherence) * 0.05

    def exchange(self):
        for cell in self.cells:
            partner = random.choice(self.cells)
            delta = (cell.coherence - partner.coherence) * 0.01
            cell.energy += delta
            partner.energy -= delta

    def step(self):
        self.broadcast()

        for cell in self.cells:
            input_signal = self.signal_bus[cell.id]
            self.signal_bus[cell.id] *= 0.9  # decay

            cell.think(input_signal)

        self.exchange()


# =========================================================
# 🧠 COGNITIVE OS RUNTIME (OPTION 3)
# =========================================================
class OmegaMeshOS:
    def __init__(self):
        self.mesh = CognitiveMesh(size=6)
        self.tick = 0
        self.global_entropy = 0.3
        self.history = []

    def update_entropy(self):
        drift = random.uniform(-0.01, 0.02)
        self.global_entropy = max(0.1, min(0.9, self.global_entropy + drift))

    def system_step(self):
        self.tick += 1

        self.update_entropy()
        self.mesh.step()

        avg_energy = sum(c.energy for c in self.mesh.cells) / len(self.mesh.cells)
        avg_coherence = sum(c.coherence for c in self.mesh.cells) / len(self.mesh.cells)

        snapshot = {
            "tick": self.tick,
            "entropy": self.global_entropy,
            "avg_energy": avg_energy,
            "avg_coherence": avg_coherence
        }

        self.history.append(snapshot)

        if len(self.history) > 200:
            self.history.pop(0)

        dominant = max(self.mesh.cells, key=lambda c: c.coherence)

        print(
            f"[Ω-MESH-OS] tick={self.tick} "
            f"entropy={self.global_entropy:.3f} "
            f"energy={avg_energy:.3f} "
            f"coherence={avg_coherence:.3f} "
            f"dominant_cell={dominant.id}"
        )


# =========================================================
# 🧠 BOOT STRAP (ALL OPTIONS ACTIVE)
# =========================================================
if __name__ == "__main__":
    osys = OmegaMeshOS()

    print("[Ω-MESH-OS] Unified Cognitive System ONLINE")

    while True:
        osys.system_step()
        time.sleep(0.4)
