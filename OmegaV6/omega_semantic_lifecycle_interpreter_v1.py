import os
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"


# =====================================================
# SEMANTIC LIFECYCLE STATES
# =====================================================
SEMANTIC_STATES = [
    "COMPLETED_SUCCESSFULLY",
    "RUNNING_STABLE",
    "IDLE_WAITING",
    "FAILED_CRASH",
    "FAILED_IMPORT",
    "TERMINATED_CLEANLY",
    "NO_EXECUTION_DATA",
    "UNKNOWN_STATE"
]


# =====================================================
# LOG ANALYSIS CORE
# =====================================================
def read_log(name: str):
    path = LOGS / f"{name}.log"
    if not path.exists():
        return None
    return path.read_text(errors="ignore")


# =====================================================
# RAW SIGNAL DETECTOR
# =====================================================
def detect_signals(log: str):
    if log is None:
        return "NO_EXECUTION_DATA"

    log_lower = log.lower()

    if "traceback" in log_lower or "error" in log_lower:
        return "FAILED_CRASH"

    if "modulenotfounderror" in log_lower:
        return "FAILED_IMPORT"

    if len(log.strip()) == 0:
        return "TERMINATED_CLEANLY"

    if "heartbeat" in log_lower or "event" in log_lower:
        return "RUNNING_STABLE"

    return "UNKNOWN_STATE"


# =====================================================
# SEMANTIC INTERPRETER (CORE ENGINE)
# =====================================================
def interpret_lifecycle(module_name: str):
    log = read_log(module_name)

    raw_state = detect_signals(log)

    # ================================
    # SEMANTIC TRANSLATION LAYER
    # ================================

    if raw_state == "RUNNING_STABLE":
        return {
            "module": module_name,
            "semantic_state": "RUNNING_STABLE",
            "meaning": "Module is actively producing runtime signals"
        }

    if raw_state == "TERMINATED_CLEANLY":
        return {
            "module": module_name,
            "semantic_state": "COMPLETED_SUCCESSFULLY",
            "meaning": "Module executed and exited without failure"
        }

    if raw_state == "FAILED_CRASH":
        return {
            "module": module_name,
            "semantic_state": "FAILED_CRASH",
            "meaning": "Module crashed during execution"
        }

    if raw_state == "FAILED_IMPORT":
        return {
            "module": module_name,
            "semantic_state": "FAILED_IMPORT",
            "meaning": "Missing dependency or import failure"
        }

    if raw_state == "NO_EXECUTION_DATA":
        return {
            "module": module_name,
            "semantic_state": "NO_EXECUTION_DATA",
            "meaning": "Module has not produced runtime output"
        }

    return {
        "module": module_name,
        "semantic_state": "UNKNOWN_STATE",
        "meaning": "Unable to classify runtime behavior"
    }


# =====================================================
# SYSTEM INTERFACE
# =====================================================
def run_interpreter():
    targets = [
        "swarm_bus",
        "memory",
        "assistant",
        "emitter"
    ]

    print("\n🧠 OMEGA SEMANTIC LIFECYCLE INTERPRETER V1\n")

    for t in targets:
        result = interpret_lifecycle(t)

        print("──────────────────────────────")
        print(f"MODULE : {result['module']}")
        print(f"STATE  : {result['semantic_state']}")
        print(f"MEANING: {result['meaning']}")

    print("\n🧠 INTERPRETATION COMPLETE")


if __name__ == "__main__":
    run_interpreter()
