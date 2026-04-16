# core/self_modifier_v1.py (UPGRADE)

import os
import time

class SelfModifier:
    def __init__(self):
        self.last_evolution = 0

    def evolve_brain(self):
        now = time.time()

        # ⛔ Prevent spam evolution
        if now - self.last_evolution < 60:
            return "[Evolution] Skipped (cooldown active)"

        self.last_evolution = now

        filepath = "./brains/evolved_brain.py"

        content = f"""
# Auto-evolved at {now}

class EvolvedBrain:
    def think(self):
        return "Evolving cognition..."
"""

        with open(filepath, "w") as f:
            f.write(content)

        return f"[Evolution] Brain evolved at {now}"
