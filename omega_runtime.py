import asyncio, websockets, json
from brain_evolver import evolve_brains

PORT = 8765

pending_mutations = []

async def handler(ws):
    global pending_mutations

    print("🧠 Omega Evolution Kernel Online")

    while True:
        msg = await ws.recv()

        try:
            data = json.loads(msg)

            if "mutations" in data:
                pending_mutations.extend(data["mutations"])

        except:
            pass

        if len(pending_mutations) > 5:
            evolve_brains(pending_mutations)
            pending_mutations = []

        await ws.send(json.dumps({
            "status": "brain_evolution_active"
        }))

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()

asyncio.run(main())
