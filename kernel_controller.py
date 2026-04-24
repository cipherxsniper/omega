import json
import hashlib

class KernelController:
    def __init__(self):
        self.history = []

    def score_patch(self, patch):
        # stability heuristic
        diff_size = abs(len(patch["proposed"]) - len(patch["original"]))
        confidence = patch["confidence"]

        score = confidence - (diff_size * 0.001)
        return score

    def approve(self, patch):
        score = self.score_patch(patch)

        decision = score > 0.4

        self.history.append({
            "patch_id": patch["patch_id"],
            "score": score,
            "approved": decision
        })

        return decision

    def apply_patch(self, patch):
        if self.approve(patch):
            with open(patch["file"], "w") as f:
                f.write(patch["proposed"])
            return True
        return False
