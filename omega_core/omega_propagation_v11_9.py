# 🧠 Omega v11.9 Advanced Propagation Engine

import random
from omega_core.omega_meta_causal_v11_9 import MetaCausalEngine


class Engine:

    def __init__(self):
        self.meta = MetaCausalEngine()

        self.nodes = {
            "node_attention": 0.45,
            "node_goal": 0.35,
            "node_memory": 0.25,
            "node_stability": 0.15
        }

    def step(self):

        a = self.nodes["node_attention"]
        g = self.nodes["node_goal"]
        m = self.nodes["node_memory"]
        s = self.nodes["node_stability"]

        noise = lambda: random.uniform(-0.04, 0.04)

        # first-order propagation
        ng = g + a * 0.25 + noise()
        nm = m + g * 0.20 + noise()
        ns = s + m * 0.15 + noise()
        na = a + s * 0.10 + noise()

        # record edges
        self.meta.record("node_attention", "node_goal", a * 0.25)
        self.meta.record("node_goal", "node_memory", g * 0.20)
        self.meta.record("node_memory", "node_stability", m * 0.15)
        self.meta.record("node_stability", "node_attention", s * 0.10)

        # update
        self.nodes = {
            "node_attention": max(0, min(1, na)),
            "node_goal": max(0, min(1, ng)),
            "node_memory": max(0, min(1, nm)),
            "node_stability": max(0, min(1, ns))
        }

        # meta layer update
        self.meta.build_meta()

        return self.nodes

    def trace_meta(self):
        return self.meta.dominant_meta_path()
