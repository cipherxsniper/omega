# 🧠 v16 RENDER HIERARCHY FIX (LOCKED PRIORITY)

import sys

def render(grid, heatmap, traces, events, particles, SIZE):

    # =========================
    # CLEAR FRAME
    # =========================
    sys.stdout.write("\033[H\033[J")

    canvas = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # =========================
    # LAYER 1 — HEATMAP (GROUND)
    # =========================
    for y in range(SIZE):
        for x in range(SIZE):
            v = heatmap[y][x]
            if v > 50:
                canvas[y][x] = "🟥"
            elif v > 30:
                canvas[y][x] = "🟧"
            elif v > 15:
                canvas[y][x] = "🟨"
            elif v > 5:
                canvas[y][x] = "🟩"

    # =========================
    # LAYER 2 — TRACES (MEMORY SCARS)
    # =========================
    for t in traces:
        x, y = t["x"], t["y"]
        if 0 <= x < SIZE and 0 <= y < SIZE:
            canvas[y][x] = "●"

    # =========================
    # LAYER 3 — EVENTS (FORCES)
    # =========================
    for e in events:
        x, y = int(e["x"]), int(e["y"])
        if 0 <= x < SIZE and 0 <= y < SIZE:
            canvas[y][x] = "✦"

    # =========================
    # LAYER 4 — PARTICLES (AGENTS - HIGHEST PRIORITY)
    # =========================
    for p in particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < SIZE and 0 <= y < SIZE:
            canvas[y][x] = p.color()

    # =========================
    # RENDER OUTPUT
    # =========================
    for row in canvas:
        print("".join(row))

    sys.stdout.flush()
