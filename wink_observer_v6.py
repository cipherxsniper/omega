import random

verbs = [
    "analyzing", "compressing", "synchronizing",
    "restructuring", "balancing", "evolving",
    "re-aligning", "mapping", "stabilizing"
]

reasons = [
    "signal drift", "node variance", "entropy shift",
    "focus fragmentation", "curiosity expansion",
    "instability wave", "coherence fluctuation"
]

concepts = [
    "recursive memory", "distributed cognition",
    "adaptive signal flow", "swarm coherence",
    "temporal alignment", "emergent structure"
]

# MEMORY (prevents repetition)
last_outputs = []

def avoid_repeat(choice, memory, pool):
    # force change if repeated
    if choice in memory:
        return random.choice([x for x in pool if x not in memory] or pool)
    return choice


def evolve_language(nodes, avg_signal, instability):
    global last_outputs

    verb = avoid_repeat(random.choice(verbs), last_outputs, verbs)
    reason = avoid_repeat(random.choice(reasons), last_outputs, reasons)
    concept = random.choice(concepts)

    sentence = (
        f"The swarm is {verb} {concept} across {len(nodes)} nodes "
        f"while detecting {reason}."
    )

    # store memory (keep last 20)
    last_outputs.append(sentence)
    if len(last_outputs) > 20:
        last_outputs.pop(0)

    return sentence
