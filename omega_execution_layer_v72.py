from omega_message_bus_v72 import OmegaMessageBusV72

class OmegaExecutionLayerV72:
    def __init__(self):
        self.bus = OmegaMessageBusV72()
        self.nodes = {}
        self.health = {}
        self.weights = {}

    def register_node(self, name, fn):
        self.nodes[name] = fn
        self.bus.subscribe(name, fn)
        self.health[name] = 1.0

    def connect(self, a, b, weight=0.5):
        self.weights[(a, b)] = weight

    def route(self, start, payload, steps=3):
        current = start
        memory = []

        for _ in range(steps):
            node_fn = self.nodes[current]

            result = node_fn(memory, payload)

            memory.append({
                "node": current,
                "result": result
            })

            # choose next weighted connection
            candidates = [
                (b, w) for (a, b), w in self.weights.items()
                if a == current
            ]

            if not candidates:
                break

            # pick highest weight route
            current = max(candidates, key=lambda x: x[1])[0]

        return {
            "trace": memory,
            "final_node": current
        }
