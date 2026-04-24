import asyncio, websockets, json, random, uuid, math

PORT = 8765

agents = []
ecosystems = []
realities = []

def new_agent(x,y):
    return {
        "id": str(uuid.uuid4()),
        "x": x,
        "y": y,
        "vx": random.uniform(-0.01,0.01),
        "vy": random.uniform(-0.01,0.01),
        "dna": str(uuid.uuid4())[:6],
        "energy": random.random(),
    }

def new_reality(x,y):
    return {
        "id": str(uuid.uuid4()),
        "x": x,
        "y": y,
        "vx": random.uniform(-0.002,0.002),
        "vy": random.uniform(-0.002,0.002),
        "radius": 0.2,
    }

# seed
for _ in range(25):
    agents.append(new_agent(random.random(), random.random()))

for _ in range(3):
    realities.append(new_reality(random.random(), random.random()))

def step():
    global agents, realities

    for r in realities:
        r["x"] += r["vx"]
        r["y"] += r["vy"]

        if r["x"] < 0 or r["x"] > 1: r["vx"] *= -1
        if r["y"] < 0 or r["y"] > 1: r["vy"] *= -1

    for a in agents:
        a["x"] += a["vx"]
        a["y"] += a["vy"]

        # bounce
        if a["x"] < 0 or a["x"] > 1: a["vx"] *= -1
        if a["y"] < 0 or a["y"] > 1: a["vy"] *= -1

        # reality influence
        for r in realities:
            dx = r["x"] - a["x"]
            dy = r["y"] - a["y"]
            dist = (dx*dx + dy*dy) ** 0.5

            if dist < r["radius"]:
                a["vx"] += dx * 0.0005
                a["vy"] += dy * 0.0005

                if random.random() < 0.01:
                    agents.append(new_agent(a["x"], a["y"]))

async def handler(ws):
    print("🧠 client connected")

    try:
        while True:
            step()

            try:
                await ws.send(json.dumps({
                    "agents": agents,
                    "ecosystems": ecosystems,
                    "realities": realities
                }))
            except Exception as e:
                print("⚠️ send failed:", e)
                break

            await asyncio.sleep(0.05)

    except websockets.exceptions.ConnectionClosed:
        print("🔌 client disconnected safely")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🌌 Omega Stable Ecosystem ONLINE")
        await asyncio.Future()

asyncio.run(main())
