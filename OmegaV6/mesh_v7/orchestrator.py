import time
import random


class MeshOrchestratorV7:

    def merge(self, frames):
        base = frames[0]

        base.setdefault("governance", {})
        base["governance"]["internet_consensus"] = sum(
            random.random() for _ in frames
        ) / len(frames)

        base["mesh_size"] = len(frames)

        return base
