import time
import random
import math


# =========================
# 🧠 PHYSICS BRAIN
# =========================
class PhysicsBrain:

    def __init__(self, brain_id):

        self.id = brain_id

        # position in cognitive space
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)

        # velocity
        self.vx = 0.0
        self.vy = 0.0

        # properties
        self.mass = random.uniform(0.5, 2.0)
        self.charge = random.choice([-1, 1])
        self.reward = 0.0

    # -------------------------
    # APPLY FORCE
    # -------------------------
    def apply_force(self, fx, fy):

        self.vx += fx / self.mass
        self.vy += fy / self.mass

    # -------------------------
    # UPDATE POSITION
    # -------------------------
    def move(self):

        self.x += self.vx
        self.y += self.vy

        # damping (prevents explosion)
        self.vx *= 0.9
        self.vy *= 0.9

    # -------------------------
    # ENERGY UPDATE
    # -------------------------
    def update(self):

        self.reward += random.uniform(0.0, 0.1)


# =========================
# 🌌 COGNITIVE FIELD
# =========================
class CognitiveField:

    def __init__(self, n=5):

        self.brains = [PhysicsBrain(f"brain_{i}") for i in range(n)]
        self.tick = 0

    # -------------------------
    # DISTANCE
    # -------------------------
    def distance(self, a, b):

        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2) + 0.01

    # -------------------------
    # FORCE COMPUTATION
    # -------------------------
    def compute_forces(self):

        for i, a in enumerate(self.brains):

            for j, b in enumerate(self.brains):

                if i == j:
                    continue

                d = self.distance(a, b)

                # attraction (gravity-like)
                attraction = (a.mass * b.mass) / (d ** 2)

                # repulsion (charge-based)
                repulsion = (a.charge * b.charge) / (d ** 2)

                force = attraction - repulsion

                dx = b.x - a.x
                dy = b.y - a.y

                norm = math.sqrt(dx**2 + dy**2) + 0.01

                fx = force * dx / norm
                fy = force * dy / norm

                a.apply_force(fx, fy)

    # -------------------------
    # CLUSTER DETECTION
    # -------------------------
    def clusters(self):

        clusters = []

        for a in self.brains:

            group = []

            for b in self.brains:

                if self.distance(a, b) < 0.5:
                    group.append(b.id)

            if len(group) > 1:
                clusters.append(group)

        return clusters

    # -------------------------
    # STEP
    # -------------------------
    def step(self):

        self.tick += 1

        self.compute_forces()

        for b in self.brains:
            b.move()
            b.update()

    # -------------------------
    # STATUS
    # -------------------------
    def status(self):

        avg_reward = sum(b.reward for b in self.brains) / len(self.brains)

        return {
            "tick": self.tick,
            "avg_reward": round(avg_reward, 3),
            "clusters": self.clusters()
        }


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":

    field = CognitiveField()

    print("[Ω-v17] COGNITIVE PHYSICS FIELD ONLINE")

    while True:

        field.step()

        if field.tick % 5 == 0:
            print("[Ω-v17]", field.status())

        time.sleep(0.5)
