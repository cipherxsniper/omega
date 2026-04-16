# OMEGA DUPLICATE INTELLIGENCE LAYER v4.1
# Converts duplication attempts into structured learning signals

import time
import uuid
from collections import defaultdict, deque
from pathlib import Path

OMEGA_ROOT = Path(__file__).resolve().parent
LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


# =========================================================
# DUPLICATE EVENT MODEL
# =========================================================
class DuplicateEvent:
    def __init__(self, name, reason, context):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.reason = reason
        self.context = context
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reason": self.reason,
            "context": self.context,
            "timestamp": self.timestamp
        }


# =========================================================
# DUPLICATE INTELLIGENCE CORE
# =========================================================
class DuplicateIntelligence:
    """
    Tracks, blocks, and learns from duplicate process attempts
    """

    def __init__(self):
        self.active_registry = set()
        self.history = deque(maxlen=500)
        self.patterns = defaultdict(int)

        self.log_file = LOG_DIR / "omega_duplicate_intel.log"

    # -------------------------
    # DETECT DUPLICATE
    # -------------------------
    def is_duplicate(self, name: str):
        return name in self.active_registry

    # -------------------------
    # REGISTER PROCESS
    # -------------------------
    def register(self, name: str):
        self.active_registry.add(name)

    # -------------------------
    # REMOVE PROCESS
    # -------------------------
    def unregister(self, name: str):
        self.active_registry.discard(name)

    # -------------------------
    # HANDLE DUPLICATE ATTEMPT
    # -------------------------
    def handle_duplicate(self, name: str, reason: str, context: dict):
        event = DuplicateEvent(name, reason, context)

        self.history.append(event.to_dict())
        self.patterns[reason] += 1

        self._log(event)

        return {
            "blocked": True,
            "event_id": event.id,
            "reason": reason,
            "message": f"Duplicate prevented: {name}"
        }

    # -------------------------
    # LOGGING
    # -------------------------
    def _log(self, event: DuplicateEvent):
        with open(self.log_file, "a") as f:
            f.write(str(event.to_dict()) + "\n")

    # -------------------------
    # ANALYTICS
    # -------------------------
    def summary(self):
        return {
            "active_processes": len(self.active_registry),
            "total_duplicate_events": len(self.history),
            "top_duplicate_reasons": sorted(
                self.patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


# =========================================================
# GLOBAL INSTANCE
# =========================================================
DUPLICATE_INTEL = DuplicateIntelligence()


# =========================================================
# SAFE PROCESS WRAPPER
# =========================================================
def safe_start_process(name: str, start_fn, context=None):
    """
    Prevents duplicate execution while preserving learning signal
    """

    context = context or {}

    if DUPLICATE_INTEL.is_duplicate(name):
        return DUPLICATE_INTEL.handle_duplicate(
            name=name,
            reason="process_already_running",
            context=context
        )

    DUPLICATE_INTEL.register(name)

    try:
        result = start_fn()
        return {
            "started": True,
            "name": name,
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e),
            "name": name
        }
    finally:
        # NOTE: caller should explicitly unregister on shutdown
        pass


# =========================================================
# SAFE SHUTDOWN
# =========================================================
def stop_process(name: str):
    DUPLICATE_INTEL.unregister(name)


# =========================================================
# TEST HOOK
# =========================================================
if __name__ == "__main__":

    def fake_worker():
        print("[Ω TEST] worker started")
        time.sleep(1)
        return "ok"

    print(safe_start_process("worker_1", fake_worker))
    print(safe_start_process("worker_1", fake_worker))  # duplicate trigger
    print(DUPLICATE_INTEL.summary())
