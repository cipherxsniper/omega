def apply_swarm_influence(p, particles):
    cx = sum(x["x"] for x in particles) / len(particles)
    cy = sum(x["y"] for x in particles) / len(particles)

    dx = cx - p["x"]
    dy = cy - p["y"]

    p["vx"] += dx * 0.001
    p["vy"] += dy * 0.001
