# 👑 Omega v17 Leadership Engine

class LeadershipEngine:

    def compute_leader_score(self, node):

        return (
            node["energy"] * 0.3 +
            node["stability"] * 0.2 +
            node["trust"] * 0.2 +
            len(node.get("memory", [])) * 0.01
        )

    def is_leader(self, node):
        return self.compute_leader_score(node) > 0.7

    def decay(self, node):
        node["energy"] *= 0.999
