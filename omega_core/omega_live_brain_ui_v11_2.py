# 🧠 Omega v11.2 LIVE BRAIN (REAL GRAPH + DISCOVERY PULSES)

import time
from rich.console import Console
from rich.live import Live
from rich.table import Table

from omega_core.omega_graph_connector_v11_2 import GraphConnector
from omega_core.file_discovery_v11_2 import FileDiscovery

console = Console()


class BrainUI:

    def __init__(self):
        self.graph = GraphConnector()
        self.discovery = FileDiscovery()

        self.nodes = {}

        self.new_pulses = []

    def update_graph_nodes(self):
        self.nodes = self.graph.get_nodes()

    def detect_new_files(self):
        new = self.discovery.scan()

        for n in new:
            self.new_pulses.append(f"📡 NEW NODE: {n}")

    def pressure_bar(self, v):
        return "█" * int(v * 20) + "░" * (20 - int(v * 20))

    def render(self):

        table = Table(title="🧠 OMEGA v11.2 LIVE GRAPH CORE")

        table.add_column("Node")
        table.add_column("Pressure")
        table.add_column("State")
        table.add_column("Signal")

        self.update_graph_nodes()

        for node in list(self.nodes.keys())[:10]:

            p = self.graph.compute_pressure(node)

            if p > 0.75:
                state = "⚠ SPLIT"
            elif p > 0.55:
                state = "ADAPT"
            elif p > 0.30:
                state = "LEARN"
            else:
                state = "STABLE"

            table.add_row(
                node,
                f"{p:.3f}",
                state,
                self.pressure_bar(p)
            )

        # show discovery pulses
        if self.new_pulses:
            table.add_row("", "", "", "")
            table.add_row("📡 DISCOVERY PULSES", "", "", "")

            for p in self.new_pulses[-3:]:
                table.add_row(p, "", "", "")

        return table

    def run(self):

        with Live(self.render(), refresh_per_second=3) as live:

            while True:

                self.detect_new_files()

                live.update(self.render())

                time.sleep(2)


if __name__ == "__main__":
    ui = BrainUI()
    ui.run()
