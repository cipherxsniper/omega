
# 🧠 OMEGA v22 — SWARM COMPETITION ECOSYSTEM

import random
import math

WIDTH = 60
HEIGHT = 20

events = []
hubs = []

# =========================
# 🧬 EVENT GENERATION
# =========================
def emit_event():
    return {
        "x": random.random() * WIDTH,
        "y": random.random() * HEIGHT,
        "strength": random.random(),
        "claimed": False
    }


# =========================
# 🟣 HUB COMPETITION SYSTEM
# =========================
def distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])


def step():
    global events, hubs

    # spawn events
    for _ in range(10):
        events.append(emit_event())

    # =========================
    # ⚔️ COMPETITION LOGIC
    # =========================
    for e in events:

        best_hub = None
        best_score = -1

        for h in hubs:

            d = distance(h, e)

            # influence = strength / distance pressure
            score = h["strength"] / (d + 1)

            if score > best_score:
                best_score = score
                best_hub = h

        # =========================
        # 🧠 CLAIM / CONTEST
        # =========================
        if best_hub and best_score > 0.15:

            # hub absorbs event
            best_hub["strength"] += e["strength"] * 0.6
            e["claimed"] = True

        else:
            # spawn new hub (territory expansion)
            hubs.append({
                "x": e["x"],
                "y": e["y"],
                "strength": e["strength"]
            })

    # =========================
    # 🧬 DECAY SYSTEM (losing hubs weaken)
    # =========================
    for h in hubs:
        h["strength"] *= 0.985  # slow decay

    # remove dead hubs
    hubs = [h for h in hubs if h["strength"] > 0.05]

    events = []


# =========================
# 🎨 RENDER (STRUCTURED FIELD)
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
            symbol = "🟣"   # dominant hub
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
# 🚀 MAIN LOOP
# =========================
for _ in range(200):
    step()
    render()



# =========================
# 🚀 SAFE EXECUTION LOOP FIX
# =========================

if __name__ == "__main__":
    import time

    for _ in range(5000):   # long-running ecosystem
        step()
        render()
        time.sleep(0.05)

