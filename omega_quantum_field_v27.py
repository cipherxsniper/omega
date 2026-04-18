import time
import random
from collections import defaultdict

# ==================================================
# 🧠 OMEGA v27 — QUANTUM LEARNING SWARM
# ==================================================

SIZE = 40
NUM = 60

FIELD = {
    "entropy": 0.5,
    "observer": 1.0
}

particles = []
memory = defaultdict(lambda: 0.0)
bonds = defaultdict(float)

# ==================================================
# 🧠 PARTICLE
# ==================================================

class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.id = random.randint(0, 999999)

    def move(self):

        # 🧠 memory-influenced velocity (LEARNING CORE)
        self.vx += memory[self.id] * 0.01
        self.vy += memory[self.id] * 0.01

        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        self.vx *= 0.97
        self.vy *= 0.97

# ==================================================
# 🧠 INIT
# ==================================================

for _ in range(NUM):
    particles.append(Particle())

# ==================================================
# 🧠 LEARNING BONDS
# ==================================================

def update_bonds():

    for i, a in enumerate(particles):
        for j, b in enumerate(particles):

            if i >= j:
                continue

            dist = abs(a.x - b.x) + abs(a.y - b.y)

            if dist < 3:

                key = (a.id, b.id)

                # strengthen bond (memory accumulation)
                bonds[key] += 0.05

                # LEARNING SIGNAL
                memory[a.id] += 0.01
                memory[b.id] += 0.01

            else:
                # decay
                bonds[(a.id, b.id)] *= 0.99

# ==================================================
# 🧠 FIELD UPDATE
# ==================================================

def update_field():
    FIELD["entropy"] *= 0.995

# ==================================================
# 🧠 RENDER (v11 style + quantum memory overlay)
# ==================================================

def render():

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:

        # observer effect (v20 influence)
        symbol = "✦" if random.random() < FIELD["observer"] else "●"

        grid[p.y][p.x] = symbol

    print("\n🧠 OMEGA v27 — QUANTUM LEARNING SWARM")
    print(f"entropy={FIELD['entropy']:.3f} bonds={len(bonds)} memory={sum(memory.values()):.2f}")

    for row in grid:
        print("".join(row))

# ==================================================
# 🧠 LOOP
# ==================================================

try:
    while True:

        for p in particles:
            p.move()

        update_bonds()
        update_field()

        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v27 STOPPED SAFELY")
