import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import hashlib

# =========================
# OMEGA EVENT BUS
# =========================
EVENT_BUS = []

def emit(event):
    EVENT_BUS.append(event)

# =========================
# GLOBAL MEMORY (DISTRIBUTED MIRROR)
# =========================
GLOBAL_MEMORY = []

def write(data):
    GLOBAL_MEMORY.append(data)

# =========================
# SIMPLE SECURITY LAYER (REALISTIC)
# =========================
def secure_payload(payload):
    raw = str(payload).encode()
    return hashlib.sha256(raw).hexdigest()

# =========================
# PARTICLE SYSTEM
# =========================
NUM = 120
SIZE = 100

colors = ["purple", "green", "teal", "pink"]

class Particle:
    def __init__(self, pid):
        self.id = pid
        self.jump = 0
        self.pos = np.random.rand(2) * SIZE
        self.vel = (np.random.rand(2) - 0.5) * 2
        self.memory = []

    def color(self):
        return colors[self.jump % len(colors)]

    def step(self):
        self.pos += self.vel
        self.pos %= SIZE

    def quantum_jump(self, node_id):
        self.jump += 1

        payload = {
            "id": self.id,
            "jump": self.jump,
            "memory": len(self.memory)
        }

        self.memory.append(payload)

        event = {
            "from": self.id,
            "to": node_id,
            "color": self.color(),
            "payload": secure_payload(payload)
        }

        emit(event)
        write(event)

        return event

particles = [Particle(i) for i in range(NUM)]

# =========================
# CLUSTERING INTELLIGENCE
# =========================
def cluster(particles):
    groups = []

    for p in particles:
        group = [o for o in particles if np.linalg.norm(p.pos - o.pos) < 15]

        if group:
            groups.append({
                "size": len(group),
                "avg_jump": np.mean([x.jump for x in group])
            })

    return groups

# =========================
# VISUALIZATION
# =========================
fig, ax = plt.subplots()
ax.set_xlim(0, SIZE)
ax.set_ylim(0, SIZE)
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

scatter = ax.scatter(
    [p.pos[0] for p in particles],
    [p.pos[1] for p in particles],
    c=[p.color() for p in particles],
    s=40
)

def update(frame):
    for p in particles:
        p.step()

        if random.random() < 0.08:
            target = random.choice(particles)
            p.quantum_jump(target.id)

    scatter.set_offsets([p.pos for p in particles])
    scatter.set_color([p.color() for p in particles])

    return scatter,

ani = animation.FuncAnimation(fig, update, interval=50, blit=True)

plt.title("OMEGA v11 DISTRIBUTED QUANTUM FIELD", color="white")
plt.show()
