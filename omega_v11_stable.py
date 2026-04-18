import random
import os
import time

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

# -------------------------
# SAFE GRID NORMALIZATION
# -------------------------
def grid_safe(x, y):
    return int(max(0, min(WIDTH - 1, x))), int(max(0, min(HEIGHT - 1, y)))

# -------------------------
# EVENT EMISSION (RANDOM FIELD)
# -------------------------
def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random()
    }

# -------------------------
# CORE STEP FUNCTION
# -------------------------
def step():
    global events, hubs

    # spawn new events
    for _ in range(10):
        events.append(emit_event())

    new_hubs = []

    for e in events:
        ex, ey = e["x"], e["y"]

        best = None
        best_d = 9999

        # find nearest hub
        for h in hubs:
            d = abs(h["x"] - ex) + abs(h["y"] - ey)
            if d < best_d:
                best = h
                best_d = d

        # absorption rule (NO memory mutation chaos)
        if best and best_d < 5:
            best["strength"] += e["strength"]
        else:
            new_hubs.append({
                "x": ex,
                "y": ey,
                "strength": e["strength"]
            })

    hubs.extend(new_hubs)
    events.clear()

# -------------------------
# SNAPSHOT RENDER (CRITICAL RULE)
# -------------------------
def render():
    os.system("clear")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # draw events
    for e in events:
        x, y = grid_safe(e["x"], e["y"])
        grid[y][x] = "✦"

    # draw hubs
    for h in hubs:
        x, y = grid_safe(h["x"], h["y"])
        s = h["strength"]

        if s > 1.5:
            grid[y][x] = "🟣"
        elif s > 0.8:
            grid[y][x] = "🟢"
        elif s > 0.3:
            grid[y][x] = "🔵"
        else:
            grid[y][x] = "⚪"

    # footer (v11 key MUST exist)
    key = "KEY: 🟣🟢🔵⚪ ●✦ v11 STABLE FIELD"
    for i, c in enumerate(key):
        if i < WIDTH:
            grid[HEIGHT - 1][i] = c

    # print frame
    for row in grid:
        print("".join(row))

# -------------------------
# MAIN LOOP
# -------------------------
while True:
    step()
    render()
    time.sleep(0.1)
