# 🧠 OMEGA VISUAL CONTRACT (LOCKED v11 KEY REQUIRED)

import random

RAINBOW = ["🟥","🟧","🟨","🟩","🟦","🟪","⚪"]

def mutate(symbol):
    if random.random() < 0.05:
        return random.choice(RAINBOW)
    return symbol
