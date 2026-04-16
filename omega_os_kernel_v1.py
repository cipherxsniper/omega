import random
import time
from collections import defaultdict


# =========================================================
# IDEA OBJECT
# =========================================================
class Idea:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.8, 1.2)
        self.age = 0

    def step(self):
        self.age += 1
        self.energy += random.uniform(-0.03, 0.03)
        self.energy -= self.age * 0.001


# =========================================================
# NODE (COGNITIVE UNIT)
# =========================================================
class Node:
    def __init__(self, name):
        self.name = name
        self.ideas = []
        self.weight = random.uniform(0.8, 1.2)

    def add_idea(self, idea):
        self.ideas.append(idea)


# =========================================================
# OMEGA KERNEL
# =========================================================
class OmegaKernel:
    def __init__(self):
        self.nodes = {}
        self.memory = defaultdict(float)
        self.memory_decay = 0.01
        self.tick = 0

    # -------------------------
    # CORE EVOLUTION
    # -------------------------
    def step(self, steps=1):
        for _ in range(steps):
            self.tick += 1

            # evolve ideas
            for node in self.nodes.values():
                for idea in node.ideas:
                    idea.step()

            # rebuild memory field (voting system)
            self.memory.clear()

            for node in self.nodes.values():
                for idea in node.ideas:
                    self.memory[idea.name] += idea.energy * node.weight

            # normalize memory
            total = sum(self.memory.values()) + 1e-9
            for k in self.memory:
                self.memory[k] /= total

            # collapse weak ideas
            for node in self.nodes.values():
                node.ideas = [
                    i for i in node.ideas
                    if self.memory.get(i.name, 0) > 0.02
                ]

    # -------------------------
    # STATE VIEW
    # -------------------------
    def print_state(self):
        print(f"\n[Ω-OS] tick={self.tick}")
        print(f"nodes={len(self.nodes)} ideas={sum(len(n.ideas) for n in self.nodes.values())}")

        top = sorted(self.memory.items(), key=lambda x: x[1], reverse=True)[:5]
        print("dominant ideas:", top)


# =========================================================
# Ω-LANG INTERPRETER
# =========================================================
class OmegaLang:
    def __init__(self, kernel):
        self.k = kernel

    def run(self, code: str):
        lines = code.strip().split("\n")

        for line in lines:
            parts = line.split()
            if not parts:
                continue

            cmd = parts[0]

            # -------------------------
            # CREATE NODE
            # -------------------------
            if cmd == "CREATE" and parts[1] == "NODE":
                name = parts[2]
                self.k.nodes[name] = Node(name)

            # -------------------------
            # CREATE IDEA
            # -------------------------
            elif cmd == "CREATE" and parts[1] == "IDEA":
                name = parts[2]
                node = random.choice(list(self.k.nodes.values()))
                node.add_idea(Idea(name))

            # -------------------------
            # LINK (simple influence boost)
            # -------------------------
            elif cmd == "LINK":
                a, b = parts[1], parts[2]
                if a in self.k.nodes and b in self.k.nodes:
                    self.k.nodes[a].weight += 0.05

            # -------------------------
            # SET PARAMETERS
            # -------------------------
            elif cmd == "SET":
                if parts[1] == "MEMORY_DECAY":
                    self.k.memory_decay = float(parts[2])

            # -------------------------
            # RUN STEPS
            # -------------------------
            elif cmd == "RUN":
                if parts[1] == "STEP":
                    self.k.step(int(parts[2]))

            # -------------------------
            # PRINT
            # -------------------------
            elif cmd == "PRINT":
                if parts[1] == "STATE":
                    self.k.print_state()


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    kernel = OmegaKernel()
    lang = OmegaLang(kernel)

    print("[Ω-OS] Omega Kernel v1 ONLINE")

    # demo boot script
    bootstrap = """
    CREATE NODE brain_A
    CREATE NODE brain_B
    CREATE IDEA entropy_core
    CREATE IDEA memory_seed
    RUN STEP 5
    PRINT STATE
    """

    lang.run(bootstrap)

    while True:
        lang.run("RUN STEP 1")
        time.sleep(1)
