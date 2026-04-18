import os
import time
import random

# -----------------------------
# OMEGA TERMINAL QUANTUM FIELD
# -----------------------------

WIDTH = 60
HEIGHT = 25
NUM_NODES = 80

# initialize particles
nodes = []
for _ in range(NUM_NODES):
    nodes.append([
        random.randint(0, WIDTH - 1),
        random.randint(0, HEIGHT - 1),
        random.choice([-1, 1]),
        random.choice([-1, 1])
    ])

def clear():
    os.system("clear")

def render():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for n in nodes:
        x, y = n[0], n[1]
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = "🟣"

    print("\n".join("".join(row) for row in grid))

def update():
    for n in nodes:
        n[0] += n[2]
        n[1] += n[3]

        # quantum wrap (torus space)
        if n[0] >= WIDTH: n[0] = 0
        if n[0] < 0: n[0] = WIDTH - 1
        if n[1] >= HEIGHT: n[1] = 0
        if n[1] < 0: n[1] = HEIGHT - 1

        # random drift (cognitive noise)
        if random.random() < 0.1:
            n[2] = random.choice([-1, 0, 1])
            n[3] = random.choice([-1, 0, 1])

while True:
    clear()
    render()
    update()
    time.sleep(0.08)
