from .mesh import SwarmMesh
from .node import SwarmNode
from .consensus import ConsensusEngine

class SwarmOrchestrator:
    def __init__(self):
        self.mesh = SwarmMesh()
        self.consensus = ConsensusEngine()

        for i in range(5):
            role = "reasoner" if i % 2 == 0 else "critic"
            self.mesh.register(SwarmNode(f"node_{i}", role))

    def run(self, input_data):
        self.mesh.broadcast(input_data)
        results = self.mesh.step()
        return self.consensus.vote(results)
