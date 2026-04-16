class OmegaNodeV720:

    def __init__(self, node_id, role="worker"):
        self.node_id = node_id
        self.role = role
        self.state = {}
        self.energy = 1.0

    def update(self, signal):
        self.state.update(signal)
        self.energy *= 0.98 + (signal.get("boost", 0.0))

    def emit(self):
        return {
            "node": self.node_id,
            "state": self.state,
            "energy": self.energy
        }
