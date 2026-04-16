import json
import threading
import os
import time


# =========================
# 🧠 OMEGA COGNITIVE BUS V1
# =========================

BUS_FILE = "omega_bus.json"
LOCK = threading.Lock()


class OmegaBus:
    def __init__(self):
        self._ensure_bus()

    # -------------------------
    # BOOTSTRAP / SELF-HEAL
    # -------------------------
    def _ensure_bus(self):
        if not os.path.exists(BUS_FILE):
            self._atomic_write({"events": []})

    # -------------------------
    # SAFE READ (CORRUPTION RESISTANT)
    # -------------------------
    def read(self):
        self._ensure_bus()

        with LOCK:
            try:
                with open(BUS_FILE, "r") as f:
                    data = json.load(f)

                # schema validation
                if not isinstance(data, dict):
                    return {"events": []}

                if "events" not in data or not isinstance(data["events"], list):
                    return {"events": []}

                return data

            except (json.JSONDecodeError, FileNotFoundError):
                # AUTO-HEAL corrupted bus
                safe = {"events": []}
                self._atomic_write(safe)
                return safe

    # -------------------------
    # WRITE EVENT (ATOMIC + LOCKED)
    # -------------------------
    def publish(self, node, signal):
        with LOCK:
            bus = self.read()

            event = {
                "node": node,
                "signal": signal,
                "ts": time.time()
            }

            bus["events"].append(event)

            # MEMORY PRESSURE CONTROL (critical for long runs)
            if len(bus["events"]) > 500:
                bus["events"] = bus["events"][-500:]

            self._atomic_write(bus)

    # -------------------------
    # ATOMIC WRITE (NO CORRUPTION POSSIBLE)
    # -------------------------
    def _atomic_write(self, bus):
        tmp_file = BUS_FILE + ".tmp"

        with open(tmp_file, "w") as f:
            json.dump(bus, f, separators=(",", ":"))

        os.replace(tmp_file, BUS_FILE)

    # -------------------------
    # OPTIONAL: STREAM EVENTS
    # -------------------------
    def tail(self, last_n=10):
        data = self.read()
        return data["events"][-last_n:]
