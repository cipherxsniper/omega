import os
import time
import random
import math

# =========================
# COLOR SYSTEM (ANSI)
# =========================

RESET = "\033[0m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

# =========================
# FILE SCANNER (OMEGA ONLY)
# =========================

def scan_omega_files():
    roots = ["./Omega", "./omega-bot", "./omega_core"]
    files = []

    for root in roots:
        if os.path.exists(root):
            for r, d, f in os.walk(root):
                for file in f:
                    if file.startswith(("Omega", "omega", "node", "core")):
                        files.append(os.path.join(r, file))

    return files[:20]


# =========================
# NODE SYSTEM
# =========================

class Node:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(5, 60)
        self.y = random.randint(3, 18)

        self.energy = random.uniform(0.3, 1.0)
        self.pressure = random.uniform(0.2, 0.9)

        self.connections = {}

    def connect(self, other):
        self.connections[other.name] = random.uniform(0.1, 1.0)

    def update(self):
        self.energy += random.uniform(-0.01, 0.01)
        self.pressure += random.uniform(-0.02, 0.02)

        self.energy = max(0.01, min(1.0, self.energy))
        self.pressure = max(0.01, min(1.0, self.pressure))


# =========================
# OMEGA FIELD ENGINE
# =========================

class OmegaV23:

    def __init__(self):

        self.nodes = [
            Node("attention"),
            Node("goal"),
            Node("memory"),
            Node("stability")
        ]

        # build connections
        for n in self.nodes:
            for m in self.nodes:
                if n != m:
                    n.connect(m)

        self.particles = []  # quantum-like data packets
        self.tick = 0

    # -------------------------
    # GENERATE "QUANTUM PARTICLES"
    # -------------------------

    def generate_particles(self):
        for _ in range(random.randint(2, 5)):
            self.particles.append({
                "from": random.choice(self.nodes).name,
                "to": random.choice(self.nodes).name,
                "intensity": random.uniform(0.3, 1.0)
            })

        self.particles = self.particles[-15:]

    # -------------------------
    # UPDATE NODES
    # -------------------------

    def update(self):
        for n in self.nodes:
            n.update()

        self.generate_particles()
        self.tick += 1

    # -------------------------
    # LEADER NODE
    # -------------------------

    def leader(self):
        return max(self.nodes, key=lambda n: n.energy * n.pressure)

    # -------------------------
    # CONNECTION COUNT
    # -------------------------

    def connection_count(self):
        return sum(len(n.connections) for n in self.nodes)

    # -------------------------
    # RENDER DASHBOARD
    # -------------------------

    def render(self):

        os.system("clear")

        print(f"{BOLD}🧠 OMEGA v23 — COGNITIVE FIELD + FILE INTROSPECTION DASHBOARD{RESET}")
        print("=" * 80)

        # FILE SYSTEM
        files = scan_omega_files()

        print(f"\n📁 ACTIVE OMEGA FILES: {len(files)}")
        for f in files:
            print(f"{CYAN}▸{RESET} {f}")

        print("\n🧠 ACTIVE NODES")

        leader = self.leader()

        for n in self.nodes:
            color = GREEN if n == leader else CYAN
            print(f"{color}{n.name:<10}{RESET} P:{n.pressure:.2f} E:{n.energy:.2f}")

        print("\n🔗 NODE CONNECTIONS")
        print(f"TOTAL CONNECTIONS: {self.connection_count()}")

        for n in self.nodes:
            conns = len(n.connections)
            print(f"{n.name:<10} → {conns} links")

        print("\n🟣 QUANTUM PARTICLE FLOW")

        for p in self.particles[-10:]:

            color = PURPLE

            print(f"{color}⚛ {p['from']} → {p['to']} | I:{p['intensity']:.2f}{RESET}")

        print("\n📊 SYSTEM STATE")
        print(f"tick: {self.tick}")
        print(f"leader: {leader.name}")

        print("\n👑 ACTIVE LEADER FIELD")
        print(f"{YELLOW}{leader.name}{RESET} dominates current cognitive space")

    # -------------------------
    # MAIN STEP
    # -------------------------

    def step(self):
        self.update()


# =========================
# RUN LOOP
# =========================

if __name__ == "__main__":

    omega = OmegaV23()

    while True:
        omega.step()
        omega.render()
        time.sleep(0.3)
