class OmegaAdaptiveRouterV72:
    def __init__(self, layer):
        self.layer = layer

    def reinforce(self, a, b, success):
        key = (a, b)

        if key not in self.layer.weights:
            self.layer.weights[key] = 0.5

        if success:
            self.layer.weights[key] = min(1.0, self.layer.weights[key] + 0.05)
        else:
            self.layer.weights[key] = max(0.1, self.layer.weights[key] - 0.05)

    def prune(self):
        # remove weak edges
        to_remove = [
            k for k, v in self.layer.weights.items()
            if v < 0.15
        ]

        for k in to_remove:
            del self.layer.weights[k]
