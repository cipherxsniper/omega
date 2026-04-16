# OMEGA INTEGRATION BRIDGE v4.1
# Connects all Omega subsystems into one event-driven runtime

import time
from pathlib import Path

# Import core systems (must already exist)
from omega_event_bus_v4 import BUS, create_event
from omega_duplicate_intel_v4_1 import DUPLICATE_INTEL

OMEGA_ROOT = Path(__file__).resolve().parent


# =========================================================
# SYSTEM NARRATOR (English layer)
# =========================================================
class Narrator:
    def speak(self, text: str):
        msg = f"[Ω NARRATOR] {time.strftime('%H:%M:%S')} → {text}"
        print(msg)

        BUS.publish(
            create_event(
                event_type="narration",
                source="narrator",
                payload={"message": text}
            )
        )


NARRATOR = Narrator()


# =========================================================
# WORKER WRAPPER (EVENT ENABLED)
# =========================================================
class WorkerBridge:
    """
    Wraps worker execution so everything becomes an event.
    """

    def register_worker(self, name: str):
        DUPLICATE_INTEL.register(name)

        NARRATOR.speak(f"Worker '{name}' registered and active")

        BUS.publish(
            create_event(
                event_type="worker_registered",
                source=name,
                payload={"status": "online"}
            )
        )

    def start_task(self, worker_name: str, task: str):
        if DUPLICATE_INTEL.is_duplicate(worker_name):
            result = DUPLICATE_INTEL.handle_duplicate(
                name=worker_name,
                reason="worker_already_active",
                context={"task": task}
            )

            BUS.publish(
                create_event(
                    event_type="duplicate_blocked",
                    source=worker_name,
                    payload=result
                )
            )

            NARRATOR.speak(f"Duplicate worker blocked: {worker_name}")
            return result

        self.register_worker(worker_name)

        BUS.publish(
            create_event(
                event_type="task_started",
                source=worker_name,
                payload={"task": task}
            )
        )

        NARRATOR.speak(f"Task started on {worker_name}: {task}")

        return {
            "status": "executed",
            "worker": worker_name,
            "task": task
        }


# =========================================================
# EVENT NORMALIZER (ensures consistency)
# =========================================================
class EventNormalizer:
    def normalize(self, event):
        """
        Ensures all events are structured and readable.
        """
        return {
            "type": event.type,
            "source": event.source,
            "payload": event.payload,
            "timestamp": event.timestamp
        }


# =========================================================
# SYSTEM HEALTH SIGNALS
# =========================================================
class HealthMonitor:
    def heartbeat(self, name: str):
        BUS.publish(
            create_event(
                event_type="heartbeat",
                source=name,
                payload={"alive": True}
            )
        )

        NARRATOR.speak(f"Heartbeat received from {name}")


# =========================================================
# GLOBAL BRIDGE OBJECTS
# =========================================================
WORKER_BRIDGE = WorkerBridge()
HEALTH = HealthMonitor()
NORMALIZER = EventNormalizer()


# =========================================================
# SYSTEM SELF-TEST
# =========================================================
if __name__ == "__main__":

    NARRATOR.speak("Integration bridge initializing")

    WORKER_BRIDGE.start_task("worker_alpha", "process_events")
    WORKER_BRIDGE.start_task("worker_alpha", "process_events")  # duplicate test

    HEALTH.heartbeat("worker_alpha")

    NARRATOR.speak("Integration bridge test complete")
