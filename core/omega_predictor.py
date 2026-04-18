class OmegaPredictor:
    """
    Simple forward state projection
    """

    def predict(self, state):
        vx, vy, activity = state

        return [
            vx * 1.05,
            vy * 1.05,
            activity * 1.02
        ]
