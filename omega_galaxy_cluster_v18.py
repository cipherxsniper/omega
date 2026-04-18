import math

# 🧠 GALAXY CLUSTER MEMORY LAYER
galaxies = []
orbit_nodes = []

def create_galaxy(x, y):
    galaxies.append({
        "x": x,
        "y": y,
        "mass": 1.0,
        "members": [],
        "spin": 0.0
    })

def assign_to_galaxy(p):
    for g in galaxies:
        dx = p.x - g["x"]
        dy = p.y - g["y"]
        d = math.sqrt(dx*dx + dy*dy)

        if d < 15:
            g["members"].append(p)
            return

def update_galaxies(particles):
    global orbit_nodes

    orbit_nodes.clear()

    # rebuild galaxy membership each step
    for g in galaxies:
        g["members"].clear()

    for p in particles:
        assign_to_galaxy(p)

    # compute galaxy physics
    for g in galaxies:
        if len(g["members"]) > 0:
            avg_x = sum(p.x for p in g["members"]) / len(g["members"])
            avg_y = sum(p.y for p in g["members"]) / len(g["members"])

            # drift galaxy center
            g["x"] = (g["x"] * 0.98) + (avg_x * 0.02)
            g["y"] = (g["y"] * 0.98) + (avg_y * 0.02)

            g["spin"] += 0.01

            orbit_nodes.append((g["x"], g["y"], g["spin"]))
