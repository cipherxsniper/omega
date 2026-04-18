import os
import time
import random
from omega_v21_core import omega_field

def render_field():
    os.system("clear")

    print("🧠 OMEGA LIVING ATTRACTOR FIELD\n")

    grid = [[" " for _ in range(60)] for _ in range(20)]

    for i, (k, v) in enumerate(omega_field["attractor_map"].items()):

        x = int((i * 7 + random.randint(0, 3)) % 60)
        y = int((v * 10 + random.randint(0, 5)) % 20)

        symbol = "●" if v < 5 else "⬤"

        grid[y][x] = symbol

    for row in grid:
        print("".join(row))

    print("\n🟣 Field particles = active attractors")

while True:
    render_field()
    time.sleep(0.5)
