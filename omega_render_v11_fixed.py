import sys

WIDTH = 60
HEIGHT = 20

def render(events, hubs):

    # HARD FRAME RESET
    sys.stdout.write("\033[H\033[J")

    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def clamp(x, y):
        return int(x) % WIDTH, int(y) % HEIGHT

    # -------------------------
    # EVENTS LAYER
    # -------------------------
    for e in events:
        x, y = clamp(e["x"], e["y"])
        grid[y][x] = "✦"

    # -------------------------
    # HUBS LAYER (STRUCTURE)
    # -------------------------
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

    # -------------------------
    # VISUAL CONTRACT (SAFE FOOTER)
    # -------------------------
    footer = "🟣🟢🔵⚪ ●✦ OMEGA v11 FIELD"
    for i in range(min(WIDTH, len(footer))):
        grid[HEIGHT - 1][i] = footer[i]

    # PRINT FRAME
    for row in grid:
        print("".join(row))
