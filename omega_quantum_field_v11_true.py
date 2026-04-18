import os
import sys
import random
import time

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

def clamp(x, y):
    return int(x) % WIDTH, int(y) % HEIGHT

def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random()
    }

def step():
    global events, hubs

    # spawn events (IMPORTANT: keep them visible this frame)
    for _ in range(10):
        events.append(emit_event())

    new_hubs = []

    for e in events:
        best = None
        best_d = 999

        for h in hubs:
            d = abs(h["x"] - e["x"]) + abs(h["y"] - e["y"])
            if d < best_d:
                best = h
                best_d = d

        if best and best_d < 5:
            best["strength"] += e["strength"]
        else:
            new_hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

    hubs.extend(new_hubs)

    # events DO NOT disappear instantly anymore (v11 behavior)
    if len(events) > 30:
        events = events[-30:]

def render():
    sys.stdout.write("\033[H\033[J")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # =========================
    # HUBS (STRUCTURE LAYER)
    # =========================
    for h in hubs:
        x, y = clamp(h["x"], h["y"])
        s = h["strength"]

        if s > 1.5:
            grid[y][x] = "🟣"
        elif s > 0.8:
            grid[y][x] = "🟢"
        elif s > 0.3:
            grid[y][x] = "🔵"
        else:
            grid[y][x] = "⚪"

    # =========================
    # EVENTS (LIVE LAYER ✦)
    # =========================
    for e in events:
        x, y = clamp(e["x"], e["y"])
        grid[y][x] = "✦"

    # =========================
    # TRAILS (NOISE LAYER ●)
    # =========================
    for _ in range(18):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if grid[y][x] == " ":
            grid[y][x] = "●"

    # footer (v11 identity MUST exist)
    key = "OMEGA v11 ●✦ STABILIZED EVENT FIELD"
    for i in range(min(WIDTH, len(key))):
        grid[HEIGHT - 1][i] = key[i]

    for row in grid:
        print("".join(row))

while True:
    step()
    render()
    time.sleep(0.1)
