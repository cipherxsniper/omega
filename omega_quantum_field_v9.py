# Omega v9 - Base Field System
import random, uuid

WIDTH, HEIGHT = 50, 20

events = []

def uid():
    return str(uuid.uuid4())[:6]

def emit():
    return {
        "x": random.randint(0, WIDTH-1),
        "y": random.randint(0, HEIGHT-1),
        "s": random.random()
    }

def step():
    global events
    for _ in range(10):
        events.append(emit())

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for e in events[-200:]:
        grid[e["y"]][e["x"]] = "✦"

    for r in grid:
        print("".join(r))

if __name__ == "__main__":
    for t in range(10):
        print(f"\nTICK {t}")
        step()
