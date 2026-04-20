cat > ~/Omega/omega_v40_brain_learning.py << 'EOF'
import os, random, hashlib, time, math
from collections import defaultdict

SIZE = 40
MAX_NODES = 120

# =========================
# ID SYSTEM
# =========================
def uid():
    return hashlib.md5(str(random.random()).encode()).hexdigest()[:6]

# =========================
# NODE (NEURON)
# =========================
class Node:
    def __init__(self, parent=None):
        self.id = uid()
        self.parent = parent

        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.energy = random.random()

        # 🧠 SYNAPTIC MEMORY (IMPORTANT UPGRADE)
        self.connections = defaultdict(float)  # node_id -> weight

        self.children = []

    # =========================
    # NODE DYNAMICS
    # =========================
    def update(self, nodes):

        # energy drift
        self.energy = max(0.05, min(1.0,
            self.energy + random.uniform(-0.08, 0.08)
        ))

        # motion
        self.x = (self.x + self.vx * self.energy) % SIZE
        self.y = (self.y + self.vy * self.energy) % SIZE

        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        # =========================
        # 🧠 LEARNING RULE (KEY UPGRADE)
        # =========================
        for other in nodes:

            if other.id == self.id:
                continue

            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1

            # interaction probability
            if dist < 6:

                # reinforcement signal
                signal = (1.0 / dist) * other.energy

                # strengthen synapse
                self.connections[other.id] += signal * 0.05

                # mutual attraction (learning influence)
                self.vx += dx * signal * 0.01
                self.vy += dy * signal * 0.01

        # decay weak memory links
        for k in list(self.connections.keys()):
            self.connections[k] *= 0.98
            if self.connections[k] < 0.01:
                del self.connections[k]

        # occasional split
        if random.random() < 0.02:
            child = Node(self.id)
            self.children.append(child)
            return child

        return None


# =========================
# SYSTEM STATE
# =========================
nodes = [Node()]

# =========================
# CLUSTER DETECTION (EMERGENT BRAIN REGIONS)
# =========================
def clusters(nodes):

    groups = defaultdict(list)

    for n in nodes:
        bucket = int(n.energy * 5)
        groups[bucket].append(n)

    return groups


# =========================
# RENDER ENGINE
# =========================
def render():

    os.system("clear")

    print("🧠 OMEGA v40 — BRAIN LEARNING MODE")
    print("="*60)

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # draw nodes
    for n in nodes:

        x, y = int(n.x), int(n.y)

        if n.energy > 0.8:
            c = "🔵"
        elif n.energy > 0.5:
            c = "🟢"
        elif n.energy > 0.2:
            c = "🟣"
        else:
            c = "⚪"

        if 0 <= x < SIZE and 0 <= y < SIZE:
            grid[y][x] = c

    for row in grid:
        print("".join(row))

    print("\n🧠 BRAIN STATE")
    print("-"*40)
    print(f"Nodes: {len(nodes)}")

    total_synapses = sum(len(n.connections) for n in nodes)
    avg_connections = total_synapses / len(nodes)

    print(f"Synapses: {total_synapses}")
    print(f"Avg connections/node: {round(avg_connections,2)}")


# =========================
# MAIN LOOP
# =========================
try:
    while True:

        new_nodes = []

        for n in nodes:
            child = n.update(nodes)
            if child:
                new_nodes.append(child)

        nodes.extend(new_nodes)

        if len(nodes) > MAX_NODES:
            nodes = nodes[-MAX_NODES:]

        render()
        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 Brain learning mode stopped safely.")
EOF