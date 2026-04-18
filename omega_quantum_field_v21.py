
import random
import time
import math

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

# =========================
# 🧠 MEMORY FIELD
# =========================
heat = [[0.0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
drift_x = [[0.0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
drift_y = [[0.0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


def clamp(v, a, b):
    return max(a, min(b, v))


def grid_safe(x, y):
    return int(clamp(x, 0, WIDTH-1)), int(clamp(y, 0, HEIGHT-1))


def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "vx": random.uniform(-1, 1),
        "vy": random.uniform(-1, 1),
        "strength": random.random()
    }


# =========================
# 🔥 MEMORY UPDATE SYSTEM
# =========================
def update_memory():
    global heat, drift_x, drift_y

    for y in range(HEIGHT):
        for x in range(WIDTH):

            # decay heat
            heat[y][x] *= 0.96

            # diffuse drift (spread memory)
            dx = drift_x[y][x]
            dy = drift_y[y][x]

            drift_x[y][x] *= 0.90
            drift_y[y][x] *= 0.90

            # slight spread to neighbors
            for ny in [-1, 0, 1]:
                for nx in [-1, 0, 1]:
                    if 0 <= y+ny < HEIGHT and 0 <= x+nx < WIDTH:
                        drift_x[y+ny][x+nx] += dx * 0.01
                        drift_y[y+ny][x+nx] += dy * 0.01


# =========================
# 🧬 PARTICLE STEP (v21 CORE UPGRADE)
# =========================
def step():
    global events, hubs

    # spawn events
    for _ in range(8):
        events.append(emit_event())

    update_memory()

    new_events = []

    for e in events:

        x, y = e["x"], e["y"]
        gx, gy = grid_safe(x, y)

        # =========================
        # 🧠 MEMORY INFLUENCE
        # =========================
        mx = drift_x[gy][gx]
        my = drift_y[gy][gx]

        # =========================
        # 🟣 HUB GRAVITY
        # =========================
        for h in hubs:
            dx = h["x"] - x
            dy = h["y"] - y
            dist = math.sqrt(dx*dx + dy*dy) + 0.001

            mx += dx / dist * 0.02 * h["strength"]
            my += dy / dist * 0.02 * h["strength"]

        # =========================
        # 🧲 APPLY MOTION
        # =========================
        e["vx"] = e["vx"] * 0.7 + mx + random.uniform(-0.1, 0.1)
        e["vy"] = e["vy"] * 0.7 + my + random.uniform(-0.1, 0.1)

        e["x"] += e["vx"]
        e["y"] += e["vy"]

        # =========================
        # 🔥 HEAT IMPACT
        # =========================
        if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
            heat[gy][gx] += e["strength"]
            drift_x[gy][gx] += e["vx"] * 0.1
            drift_y[gy][gx] += e["vy"] * 0.1

        # =========================
        # 🟣 HUB FORMATION
        # =========================
        found = False
        for h in hubs:
            d = abs(h["x"] - e["x"]) + abs(h["y"] - e["y"])
            if d < 3:
                h["strength"] += e["strength"] * 0.05
                found = True

        if not found:
            hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

        new_events.append(e)

    events = new_events


# =========================
# 🖥️ RENDER (unchanged contract preserved)
# =========================
def render():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # heat layer
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if heat[y][x] > 1.5:
                grid[y][x] = "🟨"
            elif heat[y][x] > 0.7:
                grid[y][x] = "🟧"
            elif heat[y][x] > 0.2:
                grid[y][x] = "🟩"

    # hubs
    for h in hubs:
        x, y = grid_safe(h["x"], h["y"])
        grid[y][x] = "🟣"

    # particles
    for e in events:
        x, y = grid_safe(e["x"], e["y"])
        s = e["strength"]

        if s > 0.8:
            c = "🟢"
        elif s > 0.5:
            c = "🔵"
        elif s > 0.2:
            c = "⚪"
        else:
            c = "●"

        grid[y][x] = c

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))


# =========================
# 🧠 MAIN LOOP
# =========================
for _ in range(200):
    step()
    render()
    time.sleep(0.05)

