import random
import os
import time

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

def grid_safe(x, y):
    return int(max(0, min(WIDTH-1, x))), int(max(0, min(HEIGHT-1, y)))

def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random()
    }

def step():
    global events, hubs

    # spawn events
    for _ in range(10):
        events.append(emit_event())

    # absorb logic (simple clustering)
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
    # 🧠 STRICT SNAPSHOT RENDER (v11 rule)
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for h in hubs:
        x, y = grid_safe(h["x"], h["y"])
        grid[y][x] = "●"

    os.system("clear")

    for row in grid:
        print("".join(row))

def run():
    while True:
        step()
        render()
        time.sleep(0.1)

if __name__ == "__main__":
    run()
