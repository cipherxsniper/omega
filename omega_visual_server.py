import asyncio, websockets, json, random, math, uuid

PORT = 8765
GRID = 30

particles = []

def rand_dna():
    chars = "xyz1234abcd"
    return "".join(random.choice(chars) for _ in range(6))

def create_particle(box=1):
    return {
        "id": str(uuid.uuid4()),
        "x": random.random(),
        "y": random.random(),
        "vx": random.uniform(-0.01, 0.01),
        "vy": random.uniform(-0.01, 0.01),
        "weight": random.random(),
        "state": random.choice(["A","B","C"]),
        "dna": rand_dna(),
        "trail": [],
        "box": box
    }

for _ in range(120):
    particles.append(create_particle(1))

field = [[0.0]*GRID for _ in range(GRID)]

def update_field():
    global field
    field = [[0.0]*GRID for _ in range(GRID)]
    for p in particles:
        gx = int(p["x"] * GRID)
        gy = int(p["y"] * GRID)
        if 0 <= gx < GRID and 0 <= gy < GRID:
            field[gx][gy] += p["weight"]

def mutate_dna(dna):
    i = random.randint(0, len(dna)-1)
    chars = "xyz1234abcd"
    return dna[:i] + random.choice(chars) + dna[i+1:]

def update_particles():
    global particles
    new = []

    for p in particles:
        # trail
        p["trail"].append((p["x"], p["y"]))
        if len(p["trail"]) > 15:
            p["trail"].pop(0)

        # movement
        p["x"] += p["vx"]
        p["y"] += p["vy"]

        # bounce
        if p["x"] < 0 or p["x"] > 1:
            p["vx"] *= -1
        if p["y"] < 0 or p["y"] > 1:
            p["vy"] *= -1

        # --- BOX LOGIC ---
        if p["box"] == 1 and random.random() < 0.03:
            p["box"] = 2

        elif p["box"] == 2:
            # VALIDATION + DNA mutation
            p["dna"] = mutate_dna(p["dna"])
            p["weight"] *= math.exp(random.uniform(-0.3, 0.3))

            if random.random() < 0.05:
                # HPI 1-2-3-4 branching
                for shift in [1,2,3,4]:
                    clone = p.copy()
                    clone["id"] = str(uuid.uuid4())
                    clone["dna"] = mutate_dna(p["dna"])
                    clone["weight"] *= math.exp(random.uniform(-0.5,0.5))
                    clone["box"] = 3
                    new.append(clone)

        elif p["box"] == 3 and random.random() < 0.02:
            p["box"] = random.choice([1,2])

        new.append(p)

    new.sort(key=lambda x: x["weight"], reverse=True)
    particles = new[:350]

async def handler(ws):
    while True:
        update_field()
        update_particles()

        await ws.send(json.dumps({
            "particles": particles,
            "field": field
        }))
        await asyncio.sleep(0.04)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🧠 Omega HPI Field LIVE ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
