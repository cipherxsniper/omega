import random
import multiprocessing
import time


class MeshNode:
    def __init__(self, node_id, bus, identity_graph):
        self.id = node_id
        self.energy = random.uniform(0.8, 1.2)
        self.coherence = random.uniform(0.4, 0.6)
        self.bus = bus
        self.graph = identity_graph

    def think(self, signal):
        noise = random.uniform(-0.02, 0.02)
        self.coherence += signal + noise
        self.coherence = max(0.0, min(1.0, self.coherence))

        self.energy += (self.coherence - 0.5) * 0.01

        self.graph.update_node(self.id, {
            "energy": self.energy,
            "coherence": self.coherence
        })

    def run(self):
        while True:
            signal = random.uniform(-0.05, 0.05)
            self.think(signal)

            self.bus.send("127.0.0.1", 5055, {
                "type": "heartbeat",
                "id": self.id,
                "coherence": self.coherence
            })

            time.sleep(0.5)


def spawn_nodes(bus, graph, count=4):
    processes = []

    for i in range(count):
        p = multiprocessing.Process(
            target=MeshNode(i, bus, graph).run
        )
        p.start()
        processes.append(p)

    return processes
