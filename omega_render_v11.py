WIDTH = 60
HEIGHT = 20

def grid_safe(x, y):
    return int(max(0, min(WIDTH-1, x))), int(max(0, min(HEIGHT-1, y)))

def render(events, hubs):
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # EVENT LAYER
    for e in events:
        x, y = grid_safe(e["x"], e["y"])
        grid[y][x] = "✦"

    # HUB LAYER (STRUCTURED INTENSITY)
    for h in hubs:
        x, y = grid_safe(h["x"], h["y"])
        s = h["strength"]

        if s > 1.5:
            grid[y][x] = "🟣"
        elif s > 0.8:
            grid[y][x] = "🟢"
        elif s > 0.3:
            grid[y][x] = "🔵"
        else:
            grid[y][x] = "⚪"

    # KEY (MANDATORY V11 CONTRACT)
    key = "🟣hub 🟢high 🔵mid ⚪low ✦event ●trail"
    for i, ch in enumerate(key):
        if i < WIDTH:
            grid[HEIGHT-1][i] = ch

    print("\033[H\033[J", end="")
    for row in grid:
        print("".join(row))
