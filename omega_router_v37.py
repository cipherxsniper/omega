import time
import random

from omega_graph_memory_v36 import CognitiveGraphMemory


# =========================
# 🧠 OMEGA V37 ROUTER
# =========================
class OmegaRouterV37:
    def __init__(self):
        self.graph = CognitiveGraphMemory()
        self.tick_rate = 1

    # -------------------------
    # SIMULATED NODE INPUTS
    # -------------------------
    def collect_signals(self):
        return [
            ("attention", random.uniform(0.1, 1.0)),
            ("memory", random.uniform(0.1, 1.0)),
            ("stability", random.uniform(0.1, 1.0)),
            ("goal", random.uniform(0.1, 1.0))
        ]

    # -------------------------
    # ROUTING DECISION ENGINE
    # -------------------------
    def route(self, signals):
        # strongest signal wins routing priority
        signals.sort(key=lambda x: x[1], reverse=True)
        return signals[:3]

    # -------------------------
    # GRAPH UPDATE
    # -------------------------
    def update_graph(self, routed):
        nodes = [n for n, _ in routed]

        # REQUIRED BLOCK YOU REQUESTED (INTEGRATED PROPERLY)
        self.graph.update_node("attention", 0.8)
        self.graph.update_node("memory", 0.6)

        self.graph.update_edge("attention", "memory", 1.0)

        self.graph.reinforce_batch([
            "attention",
            "memory",
            "stability"
        ])

        # dynamic reinforcement
        for n, strength in routed:
            self.graph.update_node(n, strength)

        self.graph.reinforce_batch(nodes)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        signals = self.collect_signals()
        routed = self.route(signals)

        self.update_graph(routed)

        print(
            f"[V37 ROUTER] top={routed} | "
            f"graph_nodes_updated={len(routed)}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V37] COGNITIVE ROUTER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaRouterV37().run()
