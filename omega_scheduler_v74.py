class OmegaSchedulerV74:
    def __init__(self):
        self.priority = {}
        self.last_run = {}

    def score(self, node, base_score):
        decay = 0.95 ** self.last_run.get(node, 1)
        return base_score * decay

    def choose_next(self, candidates):
        return max(
            candidates,
            key=lambda x: self.score(x["node"], x["score"])
        )
