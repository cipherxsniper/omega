
class ContradictionEngine:

    def __init__(self):
        self.conflicts = []

    def detect(self, old_belief, new_belief):
        if old_belief != new_belief:
            self.conflicts.append((old_belief, new_belief))
            return True
        return False

    def resolve(self):
        # simple resolution: keep latest + frequency bias
        resolved = {}
        for a, b in self.conflicts:
            resolved[b] = resolved.get(b, 0) + 1
        return resolved
