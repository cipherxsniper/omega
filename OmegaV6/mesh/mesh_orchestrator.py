import time
from bus.mesh_bus import MeshBus


class MeshOrchestrator:

    def __init__(self):
        self.bus = MeshBus()
        self.last_frame = None

    def aggregate(self):
        data = self.bus.read()

        if not data:
            return None

        frame = data["frame"]

        # lightweight consensus signal
        frame.setdefault("governance", {})
        frame["governance"]["mesh_consensus"] = 0.5 + (hash(str(frame)) % 100) / 200

        self.last_frame = frame
        return frame
