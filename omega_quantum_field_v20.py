import time
import random

# ==================================================
# 🧠 OBSERVER FIELD
# ==================================================
OBS = {
    "value": 1.0,
    "awareness": 0.2
}

particles = []
SIZE = 40

class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def step(self):
        # OBSERVER EFFECT:
        # particles change behavior when "watched"
        if OBS["value"] > 0.5:
            self.vx += random.uniform(-0.05, 0.05)
            self.vy += random.uniform(-0.05, 0.05)

        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx *= 0.97
        self.vy *= 0.97


def render():
    OBS["awareness"] += 0.001 * len(particles)

    print("🧠 OMEGA v20 — OBSERVER CONSCIOUSNESS FIELD")
    print(f"obs={OBS['value']:.3f} awareness={OBS['awareness']:.3f}")
    print(f"particles={len(particles)}")
    print("="*50)


for _ in range(60):
    particles.append(Particle())

try:
    while True:
        for p in particles:
            p.step()

        render()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("🧠 OMEGA v20 STOPPED SAFELY")
