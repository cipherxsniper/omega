import json
import os
import tempfile

STATE_FILE = os.path.expanduser("~/Omega/shared_brain_state.json")

class OmegaCognitionBridge:
    def read(self):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return tuple(data.get("state", [0.0, 0.0, 0.0]))
        except Exception:
            return (0.0, 0.0, 0.0)

    def write(self, state):
        try:
            # atomic write (prevents corruption)
            fd, temp_path = tempfile.mkstemp()
            with os.fdopen(fd, "w") as tmp:
                json.dump({"state": state}, tmp)

            os.replace(temp_path, STATE_FILE)

        except Exception:
            pass

    def influence_factor(self):
        vx, vy, activity = self.read()

        # normalize influence (prevents explosion)
        return min(1.0, (abs(vx) + abs(vy) + activity) * 0.05)
