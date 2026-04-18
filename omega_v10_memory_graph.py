import os
import time
import random
import math
import json
from collections import defaultdict

# =============================
# CONFIG
# =============================
MEMORY_FILE = "omega_memory_graph.json"
PARTICLE_COUNT = 120
SIZE = 50

REGIONS = ["memory", "reasoning", "attention", "explore"]

COLOR = {
    "memory": "🟣",
    "reasoning": "🔵",
    "attention": "🟢",
    "explore": "⚪"
}

# =============================
# PERSISTENT MEMORY LOAD
# =============================
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {
        "nodes": {},
        "edges": {}
    }

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f)

MEMORY = load_memory()

# =============================
# NODE (PERSISTENT IDENTITY)
# =============================
class Node:
    def __init__(self, nid):
        self.id = str(nid)

        state = MEMORY["nodes"].get(self.id, {})

        self.x = state.get("x", random.randint(0, SIZE - 1))
        self.y = state.get("y", random.randint(0, SIZE - 1))

        self.region = state.get("region", random.choice(REGIONS))
        self.energy = state.get("energy", random.random())
        self.lifetime = state.get("lifetime", 0)

        self.links = MEMORY["edges"].get(self.id, {})

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def step(self):
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        self.energy += random.uniform(-0.02, 0.02)
        self.energy = max(0, min(1, self.energy))

        self.lifetime += 1

    def influence(self):
        base = sum(self.links.values())
        return base * math.log(self.lifetime + 1)

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "region": self.region,
            "energy": self.energy,
            "lifetime": self.lifetime
        }

# =============================
# GRAPH UPDATE (REINFORCEMENT LEARNING STYLE)
# =============================
def update_graph(nodes):
    for n in nodes:
        for o in random.sample(nodes, 8):

            if n.id == o.id:
                continue

            dist = math.sqrt((n.x - o.x)**2 + (n.y - o.y)**2)

            signal = (o.energy + 0.1) / (dist + 1)

            n.links[o.id] = n.links.get(o.id, 0) * 0.95 + signal * 0.1

        # prune weak links
        n.links = {k: v for k, v in n.links.items() if v > 0.05}

        # hub reinforcement
        if n.influence() > 5:
            n.energy = min(1, n.energy + 0.01)

# =============================
# REGION EVOLUTION
# =============================
def evolve_regions(nodes):
    scores = defaultdict(float)

    for n in nodes:
        scores[n.region] += n.influence()

    dominant = max(scores, key=scores.get)

    for n in nodes:
        if random.random() < 0.01:
            n.region = dominant

# =============================
# SAVE STATE
# =============================
def persist(nodes):
    MEMORY["nodes"] = {n.id: n.serialize() for n in nodes}
    MEMORY["edges"] = {n.id: n.links for n in nodes}
    save_memory(MEMORY)

# =============================
# RENDER
# =============================
def render(nodes):
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for n in nodes:
        grid[int(n.y)][int(n.x)] = COLOR[n.region]

    os.system("clear")

    for r in grid:
        print("".join(r))

    total_links = sum(len(n.links) for n in nodes)

    print("\n" + "=" * 60)
    print("🧠 OMEGA v10 — PERSISTENT MEMORY GRAPH ENGINE")
    print("=" * 60)

    print(f"🧬 Persistent Nodes : {len(nodes)}")
    print(f"🔗 Total Edges      : {total_links}")
    print(f"💾 Memory File      : {MEMORY_FILE}")
    print("-" * 60)

    region_count = defaultdict(int)
    for n in nodes:
        region_count[n.region] += 1

    for r in REGIONS:
        print(f"{COLOR[r]} {r}: {region_count[r]}")

# =============================
# INIT
# =============================
nodes = [Node(i) for i in range(PARTICLE_COUNT)]

# =============================
# LOOP
# =============================
while True:
    for n in nodes:
        n.step()

    update_graph(nodes)
    evolve_regions(nodes)
    persist(nodes)
    render(nodes)

    time.sleep(0.08)
