import os
import time
import random

# -----------------------------
# CONFIG
# -----------------------------
SIZE = 40
NODES = 100

COLORS = ["🟣", "🟢", "🔵", "⚪", "🟡", "🟠"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# -----------------------------
# FILE GRAPH (INDEX ONCE)
# -----------------------------
FILE_GRAPH = {}

def build_file_graph():
    graph = {}

    for path in OMEGA_PATHS:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            for f in files:
                full = os.path.join(root, f)

                graph[full] = {
                    "type": "py" if f.endswith(".py") else "file",
                    "connections": []
                }

    return graph


FILE_GRAPH = build_file_graph()


# -----------------------------
# PARTICLE (COGNITIVE AGENT)
# -----------------------------
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.jump = 0
        self.state_memory = []

        self.current_file = random.choice(list(FILE_GRAPH.keys())) if FILE_GRAPH else None

    def quantum_jump(self):
        self.jump += 1

        # move to new "file node"
        if FILE_GRAPH:
            self.current_file = random.choice(list(FILE_GRAPH.keys()))

        # store only TRANSITION MEMORY (not full data)
        self.state_memory.append({
            "jump": self.jump,
            "file": self.current_file,
            "event": "transition"
        })

    def step(self):
        self.x = (self.x + random.randint(-1, 1)) % SIZE
        self.y = (self.y + random.randint(-1, 1)) % SIZE

        if random.random() < 0.10:
            self.quantum_jump()

    def color(self):
        # 🧠 multi-state quantum color system

        if self.jump == 0:
            return "🟣"

        if self.jump % 5 == 0:
            return "⚪"  # re-entry state (jump back in)

        if self.jump % 7 == 0:
            return "🟡"  # mutation state

        if self.jump % 3 == 0:
            return "🟠"  # unstable transition

        return COLORS[self.jump % len(COLORS)]


# -----------------------------
# INIT
# -----------------------------
particles = [Particle(i) for i in range(NODES)]


# -----------------------------
# RENDER
# -----------------------------
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    # -----------------------------
    # INTELLIGENCE PANEL
    # -----------------------------
    print("\n==============================")
    print("🧠 OMEGA v12 QUANTUM GRAPH")
    print("==============================")
    print(f"📦 Indexed Files: {len(FILE_GRAPH)}")
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Total Jumps  : {sum(p.jump for p in particles)}")

    # simulate "communication awareness"
    active_files = set(p.current_file for p in particles if p.current_file)

    print(f"🔗 Active File Nodes: {len(active_files)}")
    print("==============================\n")


# -----------------------------
# MAIN LOOP (NON-BLOCKING SIM)
# -----------------------------
try:
    while True:
        for p in particles:
            p.step()

        render()
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n🧠 Omega v12 stopped safely.")
