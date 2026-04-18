from omega_mesh_bus_v2 import OmegaBus
from omega_identity_graph_v2 import IdentityGraph
from omega_mesh_node_v2 import spawn_nodes
import time


class OmegaMeshOSV2:
    def __init__(self):
        self.bus = BUS
        self.graph = IdentityGraph()
        self.tick = 0
        self.messages = []

    def handle_message(self, msg):
        self.messages.append(msg)

        if len(self.messages) > 200:
            self.messages.pop(0)

    def run(self):
        print("[Ω-MESH-OS v2] Distributed cognition runtime ONLINE")

        self.bus.start_server(self.handle_message)

        spawn_nodes(self.bus, self.graph, count=4)

        while True:
            self.tick += 1

            avg = 0.0
            if self.messages:
                avg = sum(m.get("coherence", 0) for m in self.messages) / len(self.messages)

            print(
                f"[Ω-MESH-v2] tick={self.tick} "
                f"messages={len(self.messages)} "
                f"network_coherence={avg:.3f}"
            )

            self.graph.save()

            time.sleep(1)


if __name__ == "__main__":
    osys = OmegaMeshOSV2()
    osys.run()
