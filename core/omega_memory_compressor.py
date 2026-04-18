class OmegaMemoryCompressor:
    """
    Stabilizes global memory drift
    """

    def compress(self, state):
        # clamp + normalize drift
        for i in range(len(state)):
            if state[i] > 10:
                state[i] *= 0.5
            elif state[i] < -10:
                state[i] *= 0.5

        return state
