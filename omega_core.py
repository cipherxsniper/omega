import asyncio, websockets, json, random, uuid

PORT = 8765

particles = []

def new_particle():
    return {
        "id": str(uuid.uuid4()),
        "dna": "seed",
        "x": random.random(),
        "y": random.random(),
        "box": 1,
        "color": "white",
        "clones": 1
    }

# START WITH EXACTLY ONE PARTICLE
particles.append(new_particle())

def validate(p):
    # validation logic (box 2)
    score = random.random()

    p["dna"] = p["dna"][:4] + random.choice("abcd1234")
    p["id"] = str(uuid.uuid4())

    return score > 0.4

def step():
    global particles
    new = []

    for p in particles:

        # BOX 1 → BOX 2 (entry to validation)
        if p["box"] == 1:
            if random.random() < 0.05:
                p["box"] = 2

        # BOX 2 → VALIDATION GATE
        elif p["box"] == 2:
            if validate(p):
                p["box"] = 3
                p["color"] = "lime"

        # BOX 3 → EXPANSION (CLONE + QUANTUM JUMP)
        elif p["box"] == 3:
            if random.random() < 0.08:

                # CLONE SYSTEM
                for i in range(2):
                    c = dict(p)
                    c["id"] = str(uuid.uuid4())
                    c["clones"] = p["clones"] + 1
                    c["dna"] = p["dna"] + "-q"
                    c["color"] = random.choice(["cyan","magenta","lime"])

                    # quantum jump back or forward
                    c["box"] = random.choice([2,3])

                    new.append(c)

        new.append(p)

    particles = new[:200]

async def handler(ws):
    while True:
        step()
        await ws.send(json.dumps({"particles": particles}))
        await asyncio.sleep(0.05)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🧠 Omega Pipeline Active")
        await asyncio.Future()

asyncio.run(main())
