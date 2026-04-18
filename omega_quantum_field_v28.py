import time
import random
from collections import defaultdict

# ==================================================
# 🧠 OMEGA v28 — SELF-ORGANIZING INTELLIGENCE FIELD
# ==================================================

SIZE = 40
N = 60

FIELD = {
    "entropy": 0.5,
    "awareness": 0.2,
    "pressure": 1.0
}

# ==================================================
# 🧠 ECOSYSTEM CONNECTOR (Omega Brain Hook)
# ==================================================

OMEGA_BUS = {
    "signals": [],
    "memory_stream": defaultdict(float),
    "node_links": defaultdict(set)
}

# ==================================================
# 🧠 PARTICLES (NOW NETWORK NODES)
# ==================================================

class Node:
    def __init__(self):
        self.id = random.randint(1, 999999)
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.energy = 1.0

    def move(self):

        # field influence (global memory field)
        influence = OMEGA_BUS["memory_stream"][self.id] * 0.01

        self.vx += influence
        self.vy += influence

        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        self.vx *= 0.97
        self.vy *= 0.97

        self.energy *= 0.999

# ==================================================
# 🧠 INITIALIZE NETWORK
# ==================================================

nodes = [Node() for _ in range(N)]

# ==================================================
# 🧠 SELF-ORGANIZING NETWORK LOGIC
# ==================================================

def update_network():

    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):

            if i >= j:
                continue

            dist = abs(a.x - b.x) + abs(a.y - b.y)

            if dist < 4:

                # synapse formation
                OMEGA_BUS["node_links"][a.id].add(b.id)
                OMEGA_BUS["node_links"][b.id].add(a.id)

                weight = 1 / (dist + 0.1)

                OMEGA_BUS["memory_stream"][a.id] += weight
                OMEGA_BUS["memory_stream"][b.id] += weight

                a.energy += 0.01
                b.energy += 0.01

            else:
                # decay connections
                OMEGA_BUS["memory_stream"][a.id] *= 0.99
                OMEGA_BUS["memory_stream"][b.id] *= 0.99

# ==================================================
# 🧠 GLOBAL FIELD UPDATE
# ==================================================

def update_field():

    FIELD["entropy"] *= 0.995

    # awareness emerges from connectivity
    FIELD["awareness"] = len(OMEGA_BUS["node_links"]) / (N * 10)

# ==================================================
# 🧠 ECOSYSTEM SIGNAL BUS
# ==================================================

def broadcast():

    OMEGA_BUS["signals"].append({
        "nodes": len(nodes),
        "links": sum(len(v) for v in OMEGA_BUS["node_links"].values()),
        "entropy": FIELD["entropy"]
    })

    if len(OMEGA_BUS["signals"]) > 50:
        OMEGA_BUS["signals"].pop(0)

# ==================================================
# 🧠 RENDER (STATE DRIVEN ONLY)
# ==================================================

def render():

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for n in nodes:

        symbol = "✦" if n.energy > 0.5 else "●"

        grid[n.y][n.x] = symbol

    print("\n🧠 OMEGA v28 — SELF-ORGANIZING INTELLIGENCE FIELD")
    print(f"nodes={len(nodes)} links={sum(len(v) for v in OMEGA_BUS['node_links'].values())} awareness={FIELD['awareness']:.3f}")

    for row in grid:
        print("".join(row))

# ==================================================
# 🧠 MAIN LOOP (ECOSYSTEM CONNECTED)
# ==================================================

try:
    while True:

        for n in nodes:
            n.move()

        update_network()
        update_field()
        broadcast()

        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v28 STOPPED SAFELY")
