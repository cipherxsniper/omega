
# 🧠 OMEGA v23 — SELF-STABILIZING LIVE LOOP ENGINE

import random
import time

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

# =========================
# 🔑 OMEGA VISUAL CONTRACT (LOCKED)
# =========================
KEY = """
🟣 hub (dominant memory node)
🟢 high energy particle
🔵 medium energy particle
⚪ low energy particle
● trail / return path
✦ event spike
"""

# =========================
# 🧬 SAFETY: AUTO-HEAL STATE
# =========================
def safe_state():
    global events, hubs

    if events is None:
        events = []
    if hubs is None:
        hubs = []

# =========================
# 📡 EVENT SYSTEM
# =========================
def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random(),
        "claimed": False
    }

def distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

# =========================
# 🧠 SYSTEM STEP
# =========================
def step():
    global events, hubs

    safe_state()

    # spawn events
    for _ in range(8):
        events.append(emit_event())

    # hub interaction
    for e in events:

        best = None
        best_score = 0

        for h in hubs:
            d = distance(h, e)
            score = h["strength"] / (d + 1)

            if score > best_score:
                best_score = score
                best = h

        if best and best_score > 0.12:
            best["strength"] += e["strength"] * 0.5
            e["claimed"] = True
        else:
            hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

    # decay system
    for h in hubs:
        h["strength"] *= 0.986

    hubs = [h for h in hubs if h["strength"] > 0.05]

    events = []

# =========================
# 🎨 STABLE RENDER (NO ACCUMULATION)
# =========================
def render():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for e in events:
        x = int(e["x"])
        y = int(e["y"])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = "✦"

    for h in hubs:
        x = int(h["x"])
        y = int(h["y"])

        if h["strength"] > 1.5:
            symbol = "🟣"
        elif h["strength"] > 0.8:
            symbol = "🟢"
        elif h["strength"] > 0.3:
            symbol = "🔵"
        else:
            symbol = "⚪"

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = symbol

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

# =========================
# 🧠 SELF-STABILIZING LOOP
# =========================
def run():
    frame = 0

    while True:
        try:
            step()
            render()

            frame += 1

            # soft system heartbeat repair
            if frame % 200 == 0:
                hubs[:] = hubs[:100]  # prevent runaway growth

            time.sleep(0.05)

        except Exception as e:
            # 🛡 auto-recover instead of crash
            print("⚠️ Omega recovered:", e)
            time.sleep(0.2)
            continue

# =========================
# 🚀 START
# =========================
if __name__ == "__main__":
    run()

