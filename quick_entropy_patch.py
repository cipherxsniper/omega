def apply_entropy_patch(self):
    # ENTROPY REGULATOR (hard stop)
    if self.entropy > 0.85:
        self.policy["exploration_bias"] *= 0.9
        self.policy["stability_bias"] *= 1.1

    # HARD CLAMP
    if self.entropy > 0.9:
        self.entropy = 0.9
