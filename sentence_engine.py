import random

def build_sentence(concepts):
    if not concepts:
        return "🧠 Omega: No structured input detected."

    core = " + ".join(concepts)

    templates = [
        f"🧠 Omega: The system is interpreting {core} as a unified cognitive structure with interacting symbolic roles.",
        f"🧠 Omega: These elements ({core}) form an evolving reasoning graph with layered meaning and adaptive relationships.",
        f"🧠 Omega: The pattern {core} is being converted into structured intelligence through relational mapping and abstraction.",
        f"🧠 Omega: A semantic architecture is forming where {core} operates as interconnected cognitive agents."
    ]

    return random.choice(templates)
