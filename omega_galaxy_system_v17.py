import math

# 🧠 GALAXY MEMORY STATE (persistent clustering layer)
galaxies = []

class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 1.0
        self.members = []
        self.vx = 0.0
        self.vy = 0.0
        self.age = 0

    def absorb(self, p):
        self.members.append(p)
        self.mass += 0.1

    def update(self):
        self.age += 1
        self.vx *= 0.95
        self.vy *= 0.95

        # slow drift from internal pressure
        self.x += self.vx
        self.y += self.vy


# 🧠 CLUSTER DETECTION (emergent grouping)
def update_galaxies(particles):
    global galaxies

    # reset membership each frame
    for g in galaxies:
        g.members = []

    # assign particles to nearest galaxy or create new cluster
    for p in particles:
        assigned = False

        for g in galaxies:
            dx = p.x - g.x
            dy = p.y - g.y
            d = math.sqrt(dx*dx + dy*dy)

            if d < 8:  # cluster radius
                g.absorb(p)
                assigned = True
                break

        if not assigned:
            new_g = Galaxy(p.x, p.y)
            new_g.absorb(p)
            galaxies.append(new_g)

    # prune weak galaxies
    galaxies = [g for g in galaxies if len(g.members) > 1]

    # update galaxy physics
    for g in galaxies:
        g.update()


# 🧠 OPTIONAL: DEBUG VIEW HOOK (no visual change required)
def get_galaxy_state():
    return [
        {
            "x": g.x,
            "y": g.y,
            "mass": g.mass,
            "size": len(g.members),
            "age": g.age
        }
        for g in galaxies
    ]
