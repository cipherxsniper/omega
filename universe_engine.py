import random, uuid

ecosystems = []
universes = []

def create_ecosystem(seed_x, seed_y):
    return {
        "id": str(uuid.uuid4()),
        "x": seed_x,
        "y": seed_y,
        "energy": 1.0,
        "fitness": 0.5,
        "particles": 1,
        "age": 0
    }

def evaluate_ecosystems():
    global universes

    new_universes = []

    for e in ecosystems:

        # ⚔️ COMPETITION LOGIC
        e["fitness"] += (e["particles"] * 0.001) - 0.002
        e["energy"] *= 0.99
        e["age"] += 1

        # 🌌 UNIVERSAL FORK CONDITION
        if e["fitness"] > 1.2 and e["particles"] > 5:

            new_universes.append({
                "id": str(uuid.uuid4()),
                "parent_ecosystem": e["id"],
                "physics": {
                    "gravity": random.uniform(-0.002, 0.002),
                    "friction": random.uniform(0.95, 1.02),
                    "mutation": random.uniform(0.001, 0.02)
                },
                "stability": 1.0
            })

            e["fitness"] *= 0.5  # split cost

    universes.extend(new_universes)

def get_state():
    return {
        "ecosystems": ecosystems,
        "universes": universes
    }
