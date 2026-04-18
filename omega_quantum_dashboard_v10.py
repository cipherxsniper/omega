import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

from omega.core.quantum_particle import QuantumParticle

NUM = 120
FIELD = 100

particles = [QuantumParticle(i) for i in range(NUM)]

fig, ax = plt.subplots()
ax.set_xlim(0, FIELD)
ax.set_ylim(0, FIELD)
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

scatter = ax.scatter(
    [p.pos[0] for p in particles],
    [p.pos[1] for p in particles],
    c=["purple"] * NUM,
    s=40
)

def update(frame):
    colors = []

    for p in particles:
        p.pos += p.vel
        p.pos %= FIELD

        if random.random() < 0.08:
            target = random.randint(0, NUM-1)
            p.jump_to(target, {"energy": random.random()})

        colors.append(p.color())

    scatter.set_offsets([p.pos for p in particles])
    scatter.set_color(colors)

    return scatter,

ani = animation.FuncAnimation(fig, update, interval=50, blit=True)

plt.title("OMEGA QUANTUM MEMORY FIELD v1", color="white")
plt.show()
