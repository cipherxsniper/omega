import random
import os
import time
import math

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

# =========================
# v12 CORE STRUCTURES
# =========================

def clamp(x, y):
    return int(max(0, min(WIDTH - 1, x))), int(max(0, min(HEIGHT - 1, y)))

def emit_event():
    # stochastic field emission
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "vx": random.uniform(-0.5, 0.5),
        "vy": random.uniform(-0.5, 0.5),
        "strength": random.random(),
        "entropy": random.random()
    }

# =========================
# v12 PHYSICS STEP
# =========================

def step():
    global events, hubs

    # spawn events
    for _ in range(8):
        events.append(emit_event())

    new_hubs = []

    for e in events:
        # directional vector motion (quantum drift)
        e["x"] += e["vx"]
        e["y"] += e["vy"]

        # entropy-based jitter (controlled randomness)
        jitter = (e["entropy"] - 0.5) * 0.3
        e["x"] += jitter
        e["y"] += jitter

        ex, ey = e["x"], e["y"]

        best = None
        best_d = 999

        # hub attraction
        for h in hubs:
            dx = h["x"] - ex
            dy = h["y"] - ey
            d = math.sqrt(dx*dx + dy*dy)

            if d < best_d:
                best = h
                best_d = d

        # absorption + decay system
        if best and best_d < 6:
            best["strength"] += e["strength"] * 0.6
        else:
            new_hubs.append({
                "x": ex,
                "y": ey,
                "strength": e["strength"]
            })

    # hub decay (critical v12 feature)
    for h in hubs:
        h["strength"] *= 0.985  # slow decay

    hubs.extend(new_hubs)

    # entropy balancing (prevents collapse)
    if len(hubs) > 120:
        hubs = hubs[-120:]

    events.clear()

# =========================
# v12 STABLE RENDER SYSTEM
# =========================

def render():
    os.system("clear")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # hubs render
    for h in hubs:
        x, y = clamp(h["x"], h["y"])
        s = h["strength"]

        if s > 1.6:
            grid[y][x] = "🟣"
        elif s > 1.0:
            grid[y][x] = "🟢"
        elif s > 0.5:
            grid[y][x] = "🔵"
        elif s > 0.2:
            grid[y][x] = "⚪"
        else:
            grid[y][x] = "●"

    # footer (v12 lock key)
    key = "OMEGA v12 ●✦ quantum drift field stable"
    for i, c in enumerate(key):
        if i < WIDTH:
            grid[HEIGHT - 1][i] = c

    for row in grid:
        print("".join(row))

# =========================
# MAIN LOOP
# =========================

while True:
    step()
    render()
    time.sleep(0.1)
