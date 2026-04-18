
import random

RAINBOW = ["🟥","🟧","🟨","🟩","🟦","🟪","⚪"]

def mutate(symbol):
    if random.random() < 0.06:
        return random.choice(RAINBOW)
    return symbol


def render():

    # =========================
    # 🧠 LAYERS INITIALIZATION
    # =========================
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    heat = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    snapshot = []

    # =========================
    # 📡 BUILD SNAPSHOT
    # =========================
    for h in hubs:
        snapshot.append(("hub", h["x"], h["y"], h["strength"]))

    for e in events:
        snapshot.append(("event", e["x"], e["y"], e["strength"]))

    # =========================
    # 🔥 HEATMAP BUILD
    # =========================
    for e in events:
        x = int(max(0, min(WIDTH-1, e["x"])))
        y = int(max(0, min(HEIGHT-1, e["y"])))
        heat[y][x] += 1

    # =========================
    # 🧬 DRAW HEATMAP FIRST
    # =========================
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if heat[y][x] > 3:
                grid[y][x] = "🟨"
            elif heat[y][x] > 1:
                grid[y][x] = "🟧"
            elif heat[y][x] > 0:
                grid[y][x] = "🟩"

    # =========================
    # ✦ DRAW PARTICLES
    # =========================
    for t, x, y, s in snapshot:
        gx = int(max(0, min(WIDTH-1, x)))
        gy = int(max(0, min(HEIGHT-1, y)))

        if t == "hub":
            symbol = "🟣"

        else:
            if s > 0.85:
                symbol = "🟢"
            elif s > 0.6:
                symbol = "🔵"
            elif s > 0.3:
                symbol = "⚪"
            else:
                symbol = "●"

            symbol = mutate(symbol)

        grid[gy][gx] = symbol

        # =========================
        # ✦ DIAMOND SPIKE RULE
        # =========================
        if s > 0.9:
            if random.random() < 0.2:
                grid[gy][gx] = "✦"

    # =========================
    # 🖥️ FRAME RESET OUTPUT
    # =========================
    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))


