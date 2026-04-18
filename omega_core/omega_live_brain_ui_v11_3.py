# 🧠 Omega v11.3 LIVE DEPENDENCY FLOW BRAIN

import time
from rich.console import Console
from rich.live import Live
from rich.table import Table

from omega_core.omega_graph_connector_v11_2 import GraphConnector
from omega_core.file_discovery_v11_2 import FileDiscovery
from omega_core.omega_dependency_graph_v11_3 import DependencyGraph

console = Console()


class BrainUI:

    def __init__(self):

        self.graph = GraphConnector()
        self.discovery = FileDiscovery()
        self.dep = DependencyGraph()

        self.nodes = {}
        self.pulses = []

    def update(self):
        self.nodes = self.graph.get_nodes()
        self.dep.update_from_memory()
        self.dep.decay()

    def pressure_bar(self, v):
        return "█" * int(v * 20) + "░" * (20 - int(v * 20))

    def render(self):

        table = Table(title="🧠 OMEGA v11.3 DEPENDENCY FLOW BRAIN")

        table.add_column("Node")
        table.add_column("Pressure")
        table.add_column("State")
        table.add_column("Flow")

        self.update()

        edges = self.dep.get_edges()

        for node in list(self.nodes.keys())[:8]:

            p = self.graph.compute_pressure(node)

            if p > 0.75:
                state = "⚠ SPLIT"
            elif p > 0.55:
                state = "ADAPT"
            elif p > 0.30:
                state = "LEARN"
            else:
                state = "STABLE"

            # dependency flow summary
            flows = edges.get(node, {})
            top_flow = max(flows.values()) if flows else 0.0

            flow_bar = self.pressure_bar(min(1.0, top_flow))

            table.add_row(
                node,
                f"{p:.3f}",
                state,
                flow_bar
            )

        # FLOW VISUALIZATION LAYER
        table.add_row("", "", "", "")
        table.add_row("🔁 DEPENDENCY FLOW SIGNALS", "", "", "")

        shown = 0
        for a in edges:
            for b in edges[a]:

                if shown > 3:
                    break

                weight = edges[a][b]

                if weight > 0.15:
                    table.add_row(
                        f"{a} → {b}",
                        f"{weight:.2f}",
                        "FLOW",
                        "➜➜➜"
                    )
                    shown += 1

        return table

    def run(self):

        with Live(self.render(), refresh_per_second=3) as live:

            while True:
                live.update(self.render())
                time.sleep(1)


if __name__ == "__main__":
    BrainUI().run()
