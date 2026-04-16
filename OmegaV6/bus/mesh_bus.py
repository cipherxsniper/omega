import json
import time
import os

BUS_FILE = "bus/mesh_state.json"


class MeshBus:

    def write(self, node_id, frame):
        os.makedirs("bus", exist_ok=True)

        state = {
            "node_id": node_id,
            "timestamp": time.time(),
            "frame": frame
        }

        with open(BUS_FILE, "w") as f:
            json.dump(state, f)

    def read(self):
        if not os.path.exists(BUS_FILE):
            return None

        with open(BUS_FILE, "r") as f:
            return json.load(f)
