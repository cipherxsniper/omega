import os
import time
import random
import math

# -----------------------------
# OMEGA TERMINAL FIELD v2
# -----------------------------

WIDTH = 70
HEIGHT = 28
NUM_NODES = 90

# ANSI colors
RESET = "\033[0m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
RED = "\033[31m"

colors = [PURPLE, CYAN, YELLOW, WHITE]

# -----------------------------
# NODE STATE
# -----------------------------
nodes = []
for _ in range(NUM_NODES):
    nodes.append({
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 1),
        "vx": random.choice([-1, 0, 1]),
        "vy": random.choice([-1, 0, 1]),
        "color": PURPLE,
        "energy": random.random(),
        "jump": False
    })

# -----------------------------
# CLEAR SCREEN (FAST)
# -----------------------------
def clear():
    print("\033[H\033[J", end="")

# -----------------------------
# DISTANCE (CLUSTERING)
# -----------------------------
def dist(a, b):
    return math.sqrt((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2)

# -----------------------------
# UPDATE SYSTEM
# -----------------------------
def update():
    for i, n in enumerate(nodes):

        # -------------------------
        # CLUSTER INFLUENCE (local gravity)
        # -------------------------
        neighbors = 0
        avg_vx = 0
        avg_vy = 0

        for j, m in enumerate(nodes):
            if i == j:
                continue
            d = dist(n, m)
            if d < 6:  # cluster radius
                avg_vx += m["vx"]
                avg_vy += m["vy"]
                neighbors += 1

        if neighbors > 0:
            n["vx"] += avg_vx / neighbors * 0.05
            n["vy"] += avg_vy / neighbors * 0.05

        # -------------------------
        # RANDOM DRIFT (cognition noise)
        # -------------------------
        n["vx"] += (random.random() - 0.5) * 0.3
        n["vy"] += (random.random() - 0.5) * 0.3

        # clamp velocity
        n["vx"] = max(-1.5, min(1.5, n["vx"]))
        n["vy"] = max(-1.5, min(1.5, n["vy"]))

        # -------------------------
        # QUANTUM JUMP EVENT
        # -------------------------
        if random.random() < 0.02:
            n["x"] = random.randint(0, WIDTH - 1)
            n["y"] = random.randint(0, HEIGHT - 1)
            n["color"] = random.choice([RED, CYAN, YELLOW])
            n["jump"] = True
        else:
            n["jump"] = False

        # -------------------------
        # MOVE NODE
        # -------------------------
        n["x"] += int(n["vx"])
        n["y"] += int(n["vy"])

        # wrap space (quantum torus)
        n["x"] %= WIDTH
        n["y"] %= HEIGHT

        # decay color back to purple
        if not n["jump"]:
            n["color"] = PURPLE

# -----------------------------
# RENDER FIELD
# -----------------------------
def render():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for n in nodes:
        x, y = n["x"], n["y"]
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = n["color"] + "🟣" + RESET

    print("\n".join("".join(row) for row in grid))

# -----------------------------
# LOOP
# -----------------------------
while True:
    clear()
    update()
    render()
    time.sleep(0.06)
