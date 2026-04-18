class OmegaConsensus:
    """
    Stable swarm agreement layer
    """

    def merge(self, brain_outputs):
        if not brain_outputs:
            return [0.0, 0.0, 0.0]

        total = [0.0, 0.0, 0.0]
        count = len(brain_outputs)

        for b in brain_outputs:
            m = b["global_memory"]

            for i in range(3):
                total[i] += m[i]

        return [x / count for x in total]
