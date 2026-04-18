
# 🧠 OMEGA v21 FIELD STABILIZER
# fixes density collapse + restores visual coherence

import math

MAX_HEAT = 3.0
MAX_PER_CELL = 2


def clamp(v, a, b):
    return max(a, min(b, v))


# =========================
# 🔥 HEAT NORMALIZER
# =========================
def normalize_heat(heat):
    for y in range(len(heat)):
        for x in range(len(heat[0])):

            # soft decay
            heat[y][x] *= 0.92

            # hard cap (prevents saturation walls)
            if heat[y][x] > MAX_HEAT:
                heat[y][x] = MAX_HEAT


# =========================
# 🧠 POSITION NORMALIZER
# =========================
def normalize_positions(events, hubs, WIDTH, HEIGHT):

    def clamp_pos(p):
        p["x"] = clamp(p["x"], 0, WIDTH - 1)
        p["y"] = clamp(p["y"], 0, HEIGHT - 1)

    for e in events:
        clamp_pos(e)

    for h in hubs:
        clamp_pos(h)


# =========================
# 🧬 CELL DENSITY FILTER
# =========================
def limit_density(grid_positions):
    """
    prevents multiple particles stacking visually in same cell
    """

    seen = {}
    filtered = []

    for item in grid_positions:
        key = (item[0], item[1])

        if key not in seen:
            seen[key] = 0

        if seen[key] < MAX_PER_CELL:
            seen[key] += 1
            filtered.append(item)

    return filtered

