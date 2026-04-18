class GovernanceLayer:

    def __init__(self):
        self.approval_threshold = 0.66
        self.votes = {}

    def propose_change(self, change_id, proposal):
        self.votes[change_id] = {
            "proposal": proposal,
            "yes": 0,
            "no": 0
        }

    def vote(self, change_id, decision):
        if change_id not in self.votes:
            return "unknown proposal"

        if decision == "yes":
            self.votes[change_id]["yes"] += 1
        else:
            self.votes[change_id]["no"] += 1

    def resolve(self, change_id):
        v = self.votes[change_id]
        total = v["yes"] + v["no"]

        if total == 0:
            return False

        score = v["yes"] / total
        return score >= self.approval_threshold
