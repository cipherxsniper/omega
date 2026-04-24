class ConsensusEngine:
    def vote(self, results):
        if not results:
            return None

        # naive consensus = most frequent output string
        votes = {}
        for r in results:
            key = r["output"]
            votes[key] = votes.get(key, 0) + 1

        return max(votes, key=votes.get)
