# 🧠 Controlled communication bus (NOT file mutation)

class CommLayer:

    def __init__(self, memory_graph):
        self.mem = memory_graph

    def broadcast(self, node, message, strength=0.5):
        self.mem.write_memory(node, f"BROADCAST:{message}", strength)

    def exchange(self, node_a, node_b):
        a = self.mem.read_global_context(node_a)
        b = self.mem.read_global_context(node_b)

        return {
            "a_view": a,
            "b_view": b
        }
