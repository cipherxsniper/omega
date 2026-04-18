class OmegaAttention:
    """
    Scores event importance across swarm
    """

    def score(self, event):
        x = event.get("x", 0)
        y = event.get("y", 0)

        # simple but stable signal weighting
        return abs(x) + abs(y)

    def filter(self, events, threshold=0.2):
        return [e for e in events if self.score(e) >= threshold]
