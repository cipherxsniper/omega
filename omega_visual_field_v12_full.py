import os, time, random, sys, math

SIZE = 40
PARTICLES = 60

# =========================
# HEAT MEMORY FIELD
# =========================
heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def update_heat(x, y):
    heatmap[y][x] += 1

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= 0.97

def heat_char(v):
    if v > 50: return "🔥"
    if v > 30: return "🟥"
    if v > 15: return "🟧"
    if v > 8:  return "🟨"
    if v > 3:  return "🟩"
    return None


# =========================
# EVENTS
# =========================
events = []

def emit_event(x, y, strength):
    events.append({"x":x,"y":y,"s":strength,"life":8})

def decay_events():
    for e in events:
        e["life"] -= 1
        e["s"] *= 0.88
    events[:] = [e for e in events if e["life"] > 0]


# =========================
# TRAILS
# =========================
trails = []

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# =========================
# PARTICLES
# =========================
class P:
    def __init__(self):
        self.x = random.randint(0,SIZE-1)
        self.y = random.randint(0,SIZE-1)
        self.vx = random.uniform(-1,1)
        self.vy = random.uniform(-1,1)
        self.jump = 0

    def step(self):
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.1,0.1)
        self.vy += random.uniform(-0.1,0.1)

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        if random.random() < 0.05:
            self.jump += 1
            trails.append({"x":int(self.x),"y":int(self.y),"life":6})
            emit_event(int(self.x), int(self.y), 1.0)

    def c(self):
        return ["🟣","🟢","🔵","⚪"][self.jump % 4]


particles = [P() for _ in range(PARTICLES)]


# =========================
# RENDER
# =========================
def render():
    os.system("clear")

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # heat layer
    for y in range(SIZE):
        for x in range(SIZE):
            c = heat_char(heatmap[y][x])
            if c:
                grid[y][x] = c

    # trails
    for t in trails:
        grid[t["y"]][t["x"]] = "●"

    # events
    for e in events:
        grid[e["y"]][e["x"]] = "✦"

    # particles
    for p in particles:
        grid[int(p.y)][int(p.x)] = p.c()

    for row in grid:
        print("".join(row))

    print("\n🧠 OMEGA FIELD v12 FULL RESTORE")


# =========================
# LOOP
# =========================
while True:
    for p in particles:
        p.step()

    decay_heat()
    decay_trails()
    decay_events()

    render()
    time.sleep(0.12)
