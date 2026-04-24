import json, os, random, time

BRAIN_DIR = os.path.expanduser("~/Omega/brains")
EVOLUTION_LOG = os.path.expanduser("~/Omega/evolution_log.json")

def load_brain(path):
    with open(path) as f:
        return json.load(f)

def save_brain(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def mutate(value, delta):
    return max(0.0, min(1.0, value + delta))

def apply_mutation(brain, mutation):

    try:
        path = mutation["target"].split(".")
        delta = mutation["delta"]

        ref = brain
        for p in path[:-1]:
            ref = ref[p]

        key = path[-1]
        ref[key] = mutate(ref[key], delta)

        return brain

    except:
        return brain

def evolve_brains(mutations):

    try:
        files = os.listdir(BRAIN_DIR)
    except:
        return

    for f in files:
        if not f.endswith(".json"):
            continue

        path = os.path.join(BRAIN_DIR, f)
        brain = load_brain(path)

        for m in mutations:
            if random.random() < 0.5:  # SAFE LIMITER
                brain = apply_mutation(brain, m)

        brain["fitness"] = brain.get("fitness", 0) + random.uniform(-0.01, 0.02)

        save_brain(path, brain)
