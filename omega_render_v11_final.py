import os
import sys

WIDTH = 60
HEIGHT = 20

def render(events, hubs):

    # 🧠 HARD FRAME RESET (NO GHOSTING)
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # =========================
    # NORMALIZED PLACEMENT (KEY FIX)
    # =========================
    def clamp(x, y):
        return int(x) % WIDTH, int(y) % HEIGHT

    # EVENTS (✦ layer)
    for e in events:
        x, y = clamp(e["x"], e["y"])
        grid[y][x] = "✦"

    # HUBS (STRUCTURE LAYER)
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
    # VISUAL CONTRACT FOOTER (LOCKED)
    # =========================
    footer = "KEY: 🟣🟢🔵⚪ ●✦ FIELD STABLE v11"
    for i, ch in enumerate(footer):
        if i < WIDTH:
            grid[HEIGHT-1][i] = ch

    # PRINT SINGLE SNAPSHOT ONLY
    for row in grid:
        sys.stdout.write("".join(row) + "\n")

    sys.stdout.flush()
