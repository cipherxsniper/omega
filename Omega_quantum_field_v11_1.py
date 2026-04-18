import os
import sys
import random
import time
from collections import defaultdict

WIDTH = 60
HEIGHT = 20

events = []
hubs = []
connections = []

# =========================
# UTIL
# =========================
def clamp(x, y):
    return int(x) % WIDTH, int(y) % HEIGHT

def dist(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

# =========================
# EVENT SYSTEM
# =========================
def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random(),
        "size": random.random()
    }

# =========================
# STEP ENGINE
# =========================
def step():
    global events, hubs, connections

    # spawn events
    for _ in range(10):
        events.append(emit_event())

    new_hubs = []

    for e in events:
        best = None
        best_d = 999

        for h in hubs:
            d = dist(h, e)
            if d < best_d:
                best = h
                best_d = d

        # absorption
        if best and best_d < 5:
            best["strength"] += e["strength"]

            # node connection creation (v11.1 add)
            connections.append((best["x"], best["y"], e["x"], e["y"]))
        else:
            new_hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

    hubs.extend(new_hubs)

    # event lifecycle control
    if len(events) > 50:
        events = events[-50:]

# =========================
# HEATMAP GENERATION
# =========================
def heatmap():
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for h in hubs:
        x, y = clamp(h["x"], h["y"])
        grid[y][x] += h["strength"]

    return grid

# =========================
# RENDER SYSTEM
# =========================
def render():
    sys.stdout.write("\033[H\033[J")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    heat = heatmap()

    # =========================
    # HEATMAP LAYER (SQUARE FIELD)
    # =========================
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if heat[y][x] > 1.5:
                grid[y][x] = "🟧"
            elif heat[y][x] > 0.8:
                grid[y][x] = "🟨"
            elif heat[y][x] > 0.3:
                grid[y][x] = "🟩"

    # =========================
    # HUB LAYER (NODES)
    # =========================
    for h in hubs:
        x, y = clamp(h["x"], h["y"])
        s = h["strength"]

        if s > 1.5:
            grid[y][x] = "🟣"
        elif s > 0.9:
            grid[y][x] = "🟢"
        elif s > 0.4:
            grid[y][x] = "🔵"
        else:
            grid[y][x] = "⚪"

    # =========================
    # EVENT LAYER (SMALL + LARGE PARTICLES)
    # =========================
    for e in events:
        x, y = clamp(e["x"], e["y"])

        if e["size"] > 0.7:
            grid[y][x] = "✦"   # large particle
        else:
            grid[y][x] = "●"   # small particle

    # =========================
    # CONNECTION LAYER (GRAPH EDGES - simplified)
    # =========================
    for c in connections[-40:]:
        x, y = clamp(c[0], c[1])
        if grid[y][x] == " ":
            grid[y][x] = "·"

    # =========================
    # LEGEND / KEY (LOCKED)
    # =========================
    key = [
        "OMEGA v11.1 STRUCTURED FIELD",
        "🟣🟢🔵⚪ = NODES (HUBS)",
        "● = small particle",
        "✦ = large particle",
        "🟩🟨🟧 = heatmap density",
        "· = connections",
        "FILES/BRIANS/GRAPH LAYER ACTIVE"
    ]

    for i, line in enumerate(key):
        if i < HEIGHT:
            for j, c in enumerate(line[:WIDTH]):
                grid[i][j] = c

    for row in grid:
        print("".join(row))

# =========================
# MAIN LOOP
# =========================
while True:
    step()
    render()
    time.sleep(0.1)
