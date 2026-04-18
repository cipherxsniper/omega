import json
import os
import threading

class OmegaGlobalMemory:
    """
    Single shared memory space for ALL Omega brains
    (true swarm synchronization layer)
    """

    _lock = threading.Lock()
    _file = "logs/omega_global_memory.json"

    def __init__(self):
        if not os.path.exists(self._file):
            with open(self._file, "w") as f:
                json.dump({"state": [0.0, 0.0, 0.0]}, f)

    def read(self):
        with self._lock:
            with open(self._file, "r") as f:
                return json.load(f)

    def write(self, state):
        with self._lock:
            with open(self._file, "w") as f:
                json.dump({"state": state}, f)

    def update(self, vx, vy, activity):
        data = self.read()["state"]

        data[0] = data[0] * 0.95 + vx * 0.05
        data[1] = data[1] * 0.95 + vy * 0.05
        data[2] = data[2] * 0.95 + activity * 0.01

        self.write(data)
        return data
