import random

# 🌈 RAINBOW MICRO FIELD (v11 RESTORE LAYER)
RAINBOW = ["🟥","🟧","🟨","🟩","🟦","🟪","⚪"]

sparks = []

def emit_spark(x, y):
    if random.random() < 0.08:
        sparks.append({
            "x": x,
            "y": y,
            "color": random.choice(RAINBOW),
            "life": random.randint(2, 5)
        })

def decay_sparks():
    for s in sparks:
        s["life"] -= 1
    sparks[:] = [s for s in sparks if s["life"] > 0]
