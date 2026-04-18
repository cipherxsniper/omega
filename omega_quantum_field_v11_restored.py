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

    # generate events
    for _ in range(8):
        events.append(emit_event())

    # process events into hubs
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
            hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

    events.clear()

def render():
    # 🧠 HARD FRAME RESET (CRITICAL v11 BEHAVIOR)
    sys.stdout.write("\033[H\033[J")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # EVENTS (✦)
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

    # trail layer (visual noise but stable)
    for _ in range(12):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if grid[y][x] == " ":
            grid[y][x] = "●"

    for row in grid:
        print("".join(row))

# MAIN LOOP (v11 style stability loop)
while True:
    step()
    render()
    time.sleep(0.1)
