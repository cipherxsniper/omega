# OMEGA OBSERVABILITY LAYER v4.1
# Converts system behavior into human-readable intelligence logs

import time
import json
from pathlib import Path

OMEGA_ROOT = Path(__file__).resolve().parents[1]
RUNTIME = OMEGA_ROOT / "runtime"
RUNTIME.mkdir(exist_ok=True)

LOG_FILE = OMEGA_ROOT / "logs" / "omega_readable.log"
LOG_FILE.parent.mkdir(exist_ok=True)


class OmegaNarrator:
    """
    Converts system events into readable English explanations.
    """

    def say(self, message: str):
        line = f"[Ω NARRATOR] {time.strftime('%H:%M:%S')} → {message}"
        print(line)

        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


NARRATOR = OmegaNarrator()


class PIDRegistry:
    """
    Tracks all running Omega processes
    """

    def __init__(self):
        self.file = RUNTIME / "pids.json"
        self.data = self.load()

    def load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {}

    def save(self):
        self.file.write_text(json.dumps(self.data, indent=2))

    def register(self, name, pid):
        self.data[name] = {
            "pid": pid,
            "timestamp": time.time()
        }
        self.save()
        NARRATOR.say(f"Registered process '{name}' with PID {pid}")

    def remove(self, name):
        if name in self.data:
            del self.data[name]
            self.save()
            NARRATOR.say(f"Removed process '{name}' from registry")

    def get(self, name):
        return self.data.get(name)


REGISTRY = PIDRegistry()


class OmegaLock:
    """
    Ensures only ONE supervisor exists
    """

    def __init__(self):
        self.file = RUNTIME / "omega.lock"

    def acquire(self):
        if self.file.exists():
            NARRATOR.say("Lock already exists — another supervisor is running. Exiting safely.")
            return False

        self.file.write_text(str(time.time()))
        NARRATOR.say("Supervisor lock acquired.")
        return True

    def release(self):
        if self.file.exists():
            self.file.unlink()
            NARRATOR.say("Supervisor lock released.")


LOCK = OmegaLock()
