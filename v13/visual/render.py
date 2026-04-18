
def render_grid(hubs):
    grid = [[" " for _ in range(60)] for _ in range(30)]

    for h in hubs:
        x = int(h.x)
        y = int(h.y)

        activation = h.state["activation"]
        entropy = h.state["entropy"]

        if activation > 0.7:
            symbol = "◆"
        elif entropy > 0.6:
            symbol = "◇"
        else:
            symbol = "◆"

        if 0 <= y < 30 and 0 <= x < 60:
            grid[y][x] = symbol

    for row in grid:
        print("".join(row))
