from omega_mesh_node_v3 import OmegaMeshNodeV3
import time


class OmegaMeshNetworkV3:

    def __init__(self, size=4):
        self.nodes = [
            OmegaMeshNodeV3(f"node_{i}") for i in range(size)
        ]

    # ------------------------
    # GLOBAL CONSENSUS
    # ------------------------
    def consensus(self):
        scores = {}

        for node in self.nodes:
            node.step()
            strongest = node.state["strongest"]

            scores[strongest] = scores.get(strongest, 0) + 1

        return max(scores, key=scores.get)

    # ------------------------
    # MESH LOOP
    # ------------------------
    def run(self):
        while True:

            strongest_global = self.consensus()

            print({
                "global_strongest": strongest_global,
                "node_count": len(self.nodes),
                "timestamp": time.time()
            })

            # cross-sync
            for node in self.nodes:
                node.broadcast(self.nodes)

            time.sleep(1)
