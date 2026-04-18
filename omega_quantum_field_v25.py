import time
import random
import math
from collections import defaultdict

# ==================================================
# 🧠 OMEGA v25 — MOLECULAR SWARM FIELD
# ==================================================

SIZE = 40
NUM_PARTICLES = 60

rng = random.SystemRandom()

FIELD = {
    "entropy": 0.55,
    "bond_rate": 0.08,
    "break_rate": 0.03
}

particles = []
bonds = set()        # (a, b)
molecules = {}       # id -> [particle indices]


# ==================================================
# 🧠 PARTICLE (QUANTUM-INSPIRED AGENT)
# ==================================================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = rng.randint(0, SIZE - 1)
        self.y = rng.randint(0, SIZE - 1)
        self.vx = rng.uniform(-1, 1)
        self.vy = rng.uniform(-1, 1)
        self.energy = rng.random()

    def move(self):
        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        self.vx *= 0.97
        self.vy *= 0.97


# ==================================================
# 🧠 MOLECULAR PHYSICS
# ==================================================
def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


def attempt_bond(a, b):
    if (a.id, b.id) in bonds or (b.id, a.id) in bonds:
        return

    d = distance(a, b)

    # probabilistic quantum bonding
    probability = FIELD["bond_rate"] * (1.0 / (1.0 + d)) * (a.energy + b.energy)

    if rng.random() < probability:
        bonds.add((a.id, b.id))


def break_bonds():
    to_remove = []

    for (a_id, b_id) in bonds:
        a = particles[a_id]
        b = particles[b_id]

        d = distance(a, b)

        instability = FIELD["break_rate"] * d * rng.random()

        if instability > 0.6:
            to_remove.append((a_id, b_id))

    for b in to_remove:
        bonds.discard(b)


# ==================================================
# 🧠 MOLECULE BUILDER (GROUPS)
# ==================================================
def build_molecules():
    global molecules
    molecules = defaultdict(list)

    visited = set()

    def dfs(pid, mid):
        visited.add(pid)
        molecules[mid].append(pid)

        for (a, b) in bonds:
            if a == pid and b not in visited:
                dfs(b, mid)
            if b == pid and a not in visited:
                dfs(a, mid)

    mid = 0
    for p in particles:
        rebuild_molecules()  # FORCE RESYNC VISUAL STATE
        if p.id not in visited:
            dfs(p.id, mid)
            mid += 1


# ==================================================
# 🧠 EMERGENT BEHAVIOR
# ==================================================
def molecular_interactions():
        # swarm feedback loop (CRITICAL)
        for p in particles:
            p.vx += random.uniform(-0.05, 0.05)
            p.vy += random.uniform(-0.05, 0.05)

        # refresh spatial state
        molecules.clear()
        rebuild_molecules()

    for m_id, group in list(molecules.items()):

        # group energy
        energy = sum(particles[i].energy for i in group) / max(1, len(group))

        # merge behavior
        if energy > 0.7 and rng.random() < 0.02:
            FIELD["bond_rate"] += 0.001

        # split behavior
        if len(group) > 6 and energy < 0.3:
            if len(group) > 1:
                bonds.clear()  # localized decoherence


# ==================================================
# 🧠 INIT
# ==================================================
for i in range(NUM_PARTICLES):
    particles.append(Particle(i))


# ==================================================
# 🧠 LOOP
# ==================================================
    print("\n🧠 OMEGA v25 STOPPED SAFELY")

    print("\n🧠 OMEGA v25 STOPPED SAFELY")

# 🧠 MEMORY LAYER (v11 RESTORED)
trails = []

def record(p):
    trails.append({"x": p.x, "y": p.y})


# ==================================================
# 🔁 MAIN LOOP (CLEAN RESTORE)
# ==================================================

try:
    while True:

        # motion
        for p in particles:
        rebuild_molecules()  # FORCE RESYNC VISUAL STATE
            p.move()

        # bonding
        for i in range(NUM_PARTICLES):
            for j in range(i + 1, NUM_PARTICLES):
                attempt_bond(particles[i], particles[j])

        break_bonds()
        build_molecules()
        molecular_interactions()
        # swarm feedback loop (CRITICAL)
        for p in particles:
            p.vx += random.uniform(-0.05, 0.05)
            p.vy += random.uniform(-0.05, 0.05)

        # refresh spatial state
        molecules.clear()
        rebuild_molecules()


        FIELD["entropy"] *= 0.995

        # render grid
        grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

        for m_id, group in list(molecules.items()):
            for pid in group:
                p = particles[pid]
                grid[p.y][p.x] = "🟣"

        print("\n🧠 OMEGA v25 — MOLECULAR SWARM FIELD")
        print(f"molecules={len(molecules)} bonds={len(bonds)} entropy={FIELD['entropy']:.3f}")

        for row in grid:
            print("".join(row))

        time.sleep(0.15)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v25 STOPPED SAFELY")

