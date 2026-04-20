# omega_v12_quantum_particles.py

import os
import time
import random
import sys
import math
import hashlib

SIZE = 40
INITIAL_PARTICLES = 200

# =========================
# GLOBAL SYSTEM
# =========================
particles = []
events = []
trails = []

NODE_A = "A"
NODE_B = "B"
HQ     = "HQ"

# =========================
# PARTICLE CLASS (TRUE OMEGA)
# =========================
class Particle:
    def __init__(self, i, node=NODE_A):
        self.id = self.generate_id(i)
        self.node = node

        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.memory = []          # path memory
        self.id_history = [self.id]
        self.jump_count = 0

        self.dna = {
            "mutation_rate": random.uniform(0.8, 1.2),
            "curiosity": random.uniform(0.4, 1.0)
        }

    def generate_id(self, seed):
        raw = f"{seed}-{time.time()}-{random.random()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:10]

    # =========================
    # VALIDATOR (NODE 3)
    # =========================
    def validate(self):
        self.id = self.generate_id(self.id)
        self.id_history.append(self.id)

        # mutation
        self.vx *= random.uniform(0.8, 1.2)
        self.vy *= random.uniform(0.8, 1.2)

        self.dna["mutation_rate"] *= random.uniform(0.95, 1.05)

    # =========================
    # DECISION ENGINE (BEST PATH)
    # =========================
    def should_jump(self):
        if len(self.memory) < 5:
            return False

        unique_positions = len(set(self.memory))
        entropy = unique_positions / len(self.memory)

        # particle decides to expand if it's repeating too much
        return entropy < self.dna["curiosity"]

    # =========================
    # NODE TRANSITION
    # =========================
    def quantum_jump(self):
        self.validate()
        self.jump_count += 1

        # choose next node (6 possible flows simplified)
        self.node = random.choice([NODE_A, NODE_B, HQ])

        # clone
        if random.random() < 0.25:
            clone = Particle(len(particles), self.node)
            clone.x, clone.y = self.x, self.y
            particles.append(clone)

    # =========================
    # STEP FUNCTION
    # =========================
    def step(self):
        # influence from events
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1

            force = e["strength"] / dist
            self.vx += (dx/dist) * force * 0.03
            self.vy += (dy/dist) * force * 0.03

        # avoid repeating paths
        next_pos = (int(self.x + self.vx), int(self.y + self.vy))
        if next_pos in self.memory:
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-0.5, 0.5)

        # move
        self.x += self.vx
        self.y += self.vy

        self.x %= SIZE
        self.y %= SIZE

        # store memory
        self.memory.append((int(self.x), int(self.y)))
        if len(self.memory) > 50:
            self.memory.pop(0)

        # decision to jump
        if self.should_jump():
            self.quantum_jump()

            trails.append({
                "x": int(self.x),
                "y": int(self.y),
                "life": 6,
                "char": "●"
            })

            events.append({
                "x": int(self.x),
                "y": int(self.y),
                "strength": random.uniform(1, 2),
                "life": 20
            })

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[self.jump_count % len(base)]


# =========================
# INIT
# =========================
for i in range(INITIAL_PARTICLES):
    particles.append(Particle(i))

# =========================
# DECAY SYSTEMS
# =========================
def decay():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

    for e in events:
        e["life"] -= 1
        e["strength"] *= 0.9
    events[:] = [e for e in events if e["life"] > 0]


# =========================
# RENDER
# =========================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for t in trails:
        grid[t["y"]][t["x"]] = t["char"]

    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    print("\033[H\033[J", end="")
    for row in grid:
        print("".join(row))

    print("\n🧠 OMEGA v12 — TRUE PARTICLE FIELD")
    print(f"Particles: {len(particles)}")
    print(f"Total Jumps: {sum(p.jump_count for p in particles)}")
    print(f"Events: {len(events)}")

    sys.stdout.flush()


# =========================
# LOOP
# =========================
try:
    while True:
        for p in particles:
            p.step()

        decay()
        render()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped.")
