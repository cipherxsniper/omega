import os

def render(particles):
    os.system("clear")

    grid = [[" " for _ in range(40)] for _ in range(20)]

    for p in particles:
        x = int(p["x"] * 39)
        y = int(p["y"] * 19)
        grid[y][x] = "●"

    print("🧠 OMEGA FIELD LIVE\n")

    for row in grid:
        print("".join(row))

    print("\nParticles:", len(particles))
