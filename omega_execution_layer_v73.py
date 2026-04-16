from omega_message_bus_v72 import OmegaMessageBusV72
from omega_cognition_memory_v73 import OmegaCognitionMemoryV73

class OmegaExecutionLayerV73:
    def __init__(self):
        self.bus = OmegaMessageBusV72()
        self.memory = OmegaCognitionMemoryV73()

        self.nodes = {}
        self.weights = {}

    def register_node(self, name, fn):
        self.nodes[name] = fn
        self.bus.subscribe(name, fn)

    def connect(self, a, b, weight=0.5):
        self.weights[(a, b)] = weight

    def route(self, start, payload, steps=3):
        current = start
        trace = []

        for _ in range(steps):
            fn = self.nodes[current]

            result = fn(self.memory.get(current), payload)

            self.memory.record(current, payload, result)

            trace.append({
                "node": current,
                "result": result,
                "memory": self.memory.get(current)
            })

            # choose next node by weight + memory bias
            candidates = [
                (b, w) for (a, b), w in self.weights.items()
                if a == current
            ]

            if not candidates:
                break

            def score(x):
                node, weight = x
                mem = self.memory.get(node)
                return weight * mem["avg_health"]

            current = max(candidates, key=score)[0]

        return {
            "trace": trace,
            "final_node": current
        }

# ==============================
# v7.4 EMERGENT TOPOLOGY HOOK
# ==============================
from omega_emergent_patch_v74_fix import reinforce_transition, probabilistic_rewire

def apply_v74_emergent_topology(self, trace, current, health):
    if not hasattr(self, "edges"):
        return

    # reinforce transitions based on success
    if trace and len(trace) > 0:
        prev = trace[-1]["node"]
        reinforce_transition(self, prev, current, health > 0.7)

    # probabilistic graph evolution
    for node in list(self.edges.keys()):
        probabilistic_rewire(self, node)


# =========================
# v7.4 EMERGENT TOPOLOGY HOOK (SAFE)
# =========================

def _v74_hook(self, trace, current, health):
    if not hasattr(self, "edges"):
        return

    try:
        from omega_emergent_patch_v74_fix import reinforce_transition, probabilistic_rewire

        if trace and len(trace) > 0:
            prev = trace[-1]["node"]
            reinforce_transition(self, prev, current, health > 0.7)

        for node in list(self.edges.keys()):
            probabilistic_rewire(self, node)

    except Exception as e:
        # fail-safe: never crash graph
        pass

