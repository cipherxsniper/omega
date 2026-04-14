from collections import defaultdict
import random
import math

class OmegaConflictResolverV27:
    def __init__(self):
        self.brain_weights = defaultdict(lambda: 1.0)
        self.history_score = defaultdict(lambda: 1.0)

        self.step = 0

    # ---------------------------
    # REGISTER OUTCOME FEEDBACK
    # ---------------------------
    def reinforce(self, brain, success=True):
        if success:
            self.history_score[brain] += 0.05
        else:
            self.history_score[brain] *= 0.98

        # clamp stability
        self.history_score[brain] = max(0.1, min(5.0, self.history_score[brain]))

    # ---------------------------
    # COMPUTE BRAIN AUTHORITY
    # ---------------------------
    def authority(self, brain):
        return self.brain_weights[brain] * self.history_score[brain]

    # ---------------------------
    # GROUP CONFLICTS
    # ---------------------------
    def group_messages(self, messages):
        grouped = defaultdict(list)

        for m in messages:
            grouped[m["type"]].append(m)

        return grouped

    # ---------------------------
    # RESOLVE SINGLE GROUP
    # ---------------------------
    def resolve_group(self, msgs):
        if not msgs:
            return None

        weighted_sum = 0.0
        total_weight = 0.0

        for m in msgs:
            brain = m.get("brain", "unknown")
            weight = self.authority(brain)

            value = m.get("value", 1.0)

            weighted_sum += value * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight else 0.0

    # ---------------------------
    # FULL RESOLUTION STEP
    # ---------------------------
    def resolve(self, messages):
        self.step += 1

        grouped = self.group_messages(messages)

        resolved = {}

        for msg_type, msgs in grouped.items():
            resolved[msg_type] = self.resolve_group(msgs)

        return {
            "step": self.step,
            "resolved_state": resolved,
            "conflict_count": len(messages)
        }
