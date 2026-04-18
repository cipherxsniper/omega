import random

class SwarmPolicy:

    def propagate(self, brains, global_signal):

        outputs = {}

        for b in brains:
            influence = b.influence(global_signal)

            # swarm coupling effect
            swarm_bias = sum(
                brains[i].weight for i in range(len(brains))
            ) / len(brains)

            outputs[b.name] = influence + swarm_bias * 0.1

        return outputs
