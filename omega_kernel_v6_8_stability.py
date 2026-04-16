class OmegaStabilityLayer:
    def __init__(self):
        self.locked_node = None
        self.node_history = {}
        self.success_streak = {}
        self.global_score = {}

    def update_node_score(self, node, success):
        if node not in self.node_history:
            self.node_history[node] = []
            self.success_streak[node] = 0
            self.global_score[node] = 0.5

        # Track history
        self.node_history[node].append(1 if success else 0)
        if len(self.node_history[node]) > 50:
            self.node_history[node].pop(0)

        # Success streak
        if success:
            self.success_streak[node] += 1
        else:
            self.success_streak[node] = 0

        # Long-term score
        avg = sum(self.node_history[node]) / len(self.node_history[node])
        self.global_score[node] = avg

    def entropy_governor(self, kernel):
        if kernel.entropy > 0.85:
            kernel.policy["exploration_bias"] *= 0.85
            kernel.policy["stability_bias"] *= 1.15

        if kernel.entropy > 0.9:
            kernel.entropy = 0.9

    def try_lock_node(self):
        # Lock dominant stable node
        for node, score in self.global_score.items():
            if score > 0.7 and self.success_streak[node] >= 3:
                self.locked_node = node

    def apply_lock(self, kernel):
        if self.locked_node:
            kernel.policy["attention"][self.locked_node] *= 1.25

    def adaptive_learning_rate(self, kernel, success):
        if success:
            kernel.learning_rate *= 0.98
        else:
            kernel.learning_rate *= 1.02

        kernel.learning_rate = max(0.001, min(kernel.learning_rate, 0.1))

    def step(self, kernel, chosen_node, success):
        self.update_node_score(chosen_node, success)
        self.entropy_governor(kernel)
        self.try_lock_node()
        self.apply_lock(kernel)
        self.adaptive_learning_rate(kernel, success)

        return self.locked_node
