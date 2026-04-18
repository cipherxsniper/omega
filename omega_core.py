
# =========================
# NEURON ATTRACTORS v12
# =========================

class Attractor:
    def __init__(self, x=None, y=None, parent=False):
        self.x = x if x is not None else random.randint(0, SIZE-1)
        self.y = y if y is not None else random.randint(0, SIZE-1)

        self.strength = random.uniform(1.0, 2.5)
        self.energy = random.uniform(0.5, 1.5)
        self.age = 0

        self.division_threshold = random.uniform(6.0, 10.0)
        self.death_threshold = 0.3

    def drift(self):
        self.age += 1
        self.x += random.uniform(-0.15, 0.15)
        self.y += random.uniform(-0.15, 0.15)
        self.x %= SIZE
        self.y %= SIZE
        self.energy *= 0.985

    def absorb(self, amount):
        self.energy += amount

    def should_split(self):
        return self.energy > self.division_threshold

    def should_die(self):
        return self.energy < self.death_threshold and self.age > 50

    def split(self):
        child = Attractor(self.x, self.y, parent=True)
        child.strength = self.strength * random.uniform(0.8, 1.2)
        child.energy = self.energy * 0.4

        child.division_threshold = self.division_threshold * random.uniform(0.9, 1.1)
        child.x += random.uniform(-1, 1)
        child.y += random.uniform(-1, 1)

        self.energy *= 0.5
        return child


# =========================
# INITIAL ATTRACTORS
# =========================
attractors = [Attractor() for _ in range(6)]


# =========================
# ATTRACTOR EVOLUTION ENGINE
# =========================
def update_attractors():
    global attractors

    new_nodes = []

    for a in attractors:
        a.drift()

        if a.should_split() and len(attractors) < 40:
            new_nodes.append(a.split())

        if not a.should_die():
            new_nodes.append(a)

    attractors = new_nodes


# =========================
# PARTICLE → ATTRACTOR ENERGY FEED
# =========================
def feed_attractors(particle):
    for a in attractors:
        dx = a.x - particle.x
        dy = a.y - particle.y
        d = (dx*dx + dy*dy) ** 0.5 + 0.1

        if d < 4:
            a.absorb((1.0 / d) * 0.08)


# CALL THIS INSIDE Particle.step()
def attractor_interaction(self):
    for a in attractors:
        dx = a.x - self.x
        dy = a.y - self.y
        d = (dx*dx + dy*dy) ** 0.5 + 0.001

        force = a.strength / (d*d)

        self.vx += (dx/d) * force * 0.03
        self.vy += (dy/d) * force * 0.03

        if d < 4:
            a.absorb(0.05 / d)


# =========================
# NEURAL UPDATE HOOK
# =========================
def omega_neural_tick():
    update_attractors()


# =========================
# ATTRACTOR RENDERING
# =========================
def render_attractors(grid):
    for a in attractors:
        if a.energy > 8:
            symbol = "⚛️"
        elif a.energy > 4:
            symbol = "◎"
        else:
            symbol = "○"

        grid[int(a.y)][int(a.x)] = symbol

