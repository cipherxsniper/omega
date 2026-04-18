import os
import time
import random

# =========================
# COLOR SYSTEM
# =========================

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
BOLD = "\033[1m"

# =========================
# CLEAN PRINT HELPERS
# =========================

def line():
    print("─" * 90)

def section(title):
    print(f"\n{BOLD}{CYAN}[ {title} ]{RESET}")
    line()

def bar(value):
    blocks = int(value * 10)
    return "█" * blocks + "░" * (10 - blocks)

# =========================
# NODE SYSTEM
# =========================

class Node:
    def __init__(self, name):
        self.name = name
        self.p = random.uniform(0.3, 0.9)
        self.e = random.uniform(0.3, 0.9)

    def update(self):
        self.p += random.uniform(-0.03, 0.03)
        self.e += random.uniform(-0.03, 0.03)

        self.p = max(0.01, min(1.0, self.p))
        self.e = max(0.01, min(1.0, self.e))


# =========================
# OMEGA ENGINE
# =========================

class Omega:

    def __init__(self):
        self.nodes = [
            Node("attention"),
            Node("goal"),
            Node("memory"),
            Node("stability")
        ]

        self.tick = 0

    # -------------------------
    # LEADER
    # -------------------------

    def leader(self):
        return max(self.nodes, key=lambda n: n.p * n.e)

    # -------------------------
    # FLOW ENGINE (SIMULATED)
    # -------------------------

    def flow(self):
        return [
            ("attention", "stability", random.uniform(1, 8)),
            ("goal", "memory", random.uniform(1, 8)),
            ("memory", "stability", random.uniform(1, 8)),
            ("stability", "goal", random.uniform(1, 8))
        ]

    # -------------------------
    # FILE SCAN (OMEGA ONLY)
    # -------------------------

    def scan(self):
        paths = []

        base = "./omega-bot"
        if os.path.exists(base):
            for f in os.listdir(base):
                if "omega" in f or "node" in f:
                    paths.append(f"./omega-bot/{f}")

        return paths[:10]

    # -------------------------
    # RENDER DASHBOARD
    # -------------------------

    def render(self):

        os.system("clear")

        leader = self.leader()

        # =========================
        # CORE STATE
        # =========================

        section("COGNITIVE CORE")

        for n in self.nodes:
            tag = "👑" if n == leader else "●"
            print(f"{tag} {n.name:<10} P:{bar(n.p)} {n.p:.2f}  E:{bar(n.e)} {n.e:.2f}")

        # =========================
        # FLOW MAP
        # =========================

        section("COGNITIVE FLOW MAP")

        for f, t, w in self.flow():
            print(f"{PURPLE}🟣{RESET} {f:<10} → {t:<10} intensity: {w:.2f}")

        # =========================
        # FILE SYSTEM
        # =========================

        section("OMEGA FILE INTROSPECTION")

        files = self.scan()
        print(f"{GREEN}ACTIVE FILES: {len(files)}{RESET}")

        for i, f in enumerate(files):
            print(f"  [{i}] {f}")

        # =========================
        # LEADER PANEL
        # =========================

        section("LEADER STATE")

        print(f"{YELLOW}👑 DOMINANT NODE:{RESET} {leader.name}")
        print(f"P={leader.p:.2f} | E={leader.e:.2f}")

        # =========================
        # SYSTEM SUMMARY
        # =========================

        section("SYSTEM SUMMARY")

        print(f"tick: {self.tick}")
        print("status: stable cognitive flow simulation")

    # -------------------------
    # STEP
    # -------------------------

    def step(self):
        for n in self.nodes:
            n.update()

        self.tick += 1


# =========================
# RUN LOOP
# =========================

if __name__ == "__main__":

    omega = Omega()

    while True:
        omega.step()
        omega.render()
        time.sleep(0.3)
