# 🧠 Omega v11 Live Brain UI (Terminal Neural Graph)

import time
import random
import os

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text

console = Console()

# fake-but-pluggable graph view (connects to your real system later)
class BrainUI:

    def __init__(self):
        self.nodes = {
            "memory": 0.55,
            "goal": 0.62,
            "attention": 0.48,
            "stability": 0.71
        }

        self.counter = 0

    def evolve_visual_state(self):
        # simulate pressure drift (replace with real Omega graph later)
        for k in self.nodes:
            drift = random.uniform(-0.03, 0.05)
            self.nodes[k] = max(0.05, min(1.0, self.nodes[k] + drift))

    def pressure_bar(self, value):
        blocks = int(value * 20)
        return "█" * blocks + "░" * (20 - blocks)

    def render(self):

        table = Table(title="🧠 OMEGA v11 LIVE BRAIN")

        table.add_column("Node")
        table.add_column("Pressure")
        table.add_column("State")
        table.add_column("Heat")

        for node, val in self.nodes.items():

            if val > 0.75:
                state = "⚠ SPLIT"
            elif val > 0.55:
                state = "ADAPT"
            elif val > 0.35:
                state = "LEARN"
            else:
                state = "STABLE"

            heat = self.pressure_bar(val)

            table.add_row(
                node,
                f"{val:.3f}",
                state,
                heat
            )

        return table

    def run(self):

        with Live(self.render(), refresh_per_second=4) as live:

            while True:
                self.counter += 1
                self.evolve_visual_state()

                live.update(self.render())
                time.sleep(0.5)


if __name__ == "__main__":
    ui = BrainUI()
    ui.run()
