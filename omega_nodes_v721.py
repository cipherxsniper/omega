class OmegaNodeV721:

    def __init__(self, node_id):
        self.node_id = node_id
        self.state = {}
        self.influence = 1.0

    def update(self, global_memory):

        # nodes are influenced by shared field
        for k, v in global_memory.items():

            if v["weight"] > 1.5:
                self.influence += 0.01

            if k not in self.state:
                self.state[k] = v["value"]

        self.influence = min(self.influence, 3.0)

    def emit(self):
        return {
            "node": self.node_id,
            "state": self.state,
            "influence": self.influence
        }
