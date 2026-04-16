import time
import random
from bus.mesh_bus import MeshBus


class OmegaNodeV6:

    def __init__(self, node_id, engine):
        self.node_id = node_id
        self.engine = engine
        self.bus = MeshBus()

    def step(self):
        frame = self.engine.step()

        # inject node identity drift
        frame["node_id"] = self.node_id
        frame.setdefault("memory", {}).setdefault("events", []).append({
            "t": time.time(),
            "type": f"node_tick_{self.node_id}"
        })

        self.bus.write(self.node_id, frame)

        return frame
