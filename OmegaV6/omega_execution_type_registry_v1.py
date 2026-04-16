import os
import subprocess
import time
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)


# =====================================================
# EXECUTION TYPE MODEL
# =====================================================
EXECUTION_TYPES = {
    "SERVICE": {
        "keywords": ["swarm_bus", "bus", "server", "listener", "loop", "watchdog", "assistant"]
    },
    "TASK": {
        "keywords": ["emitter", "snapshot", "memory_dump", "analyzer", "test_", "probe"]
    },
    "HYBRID": {
        "keywords": ["orchestrator", "launcher", "runner", "bootstrap"]
    }
}


# =====================================================
# CLASSIFIER
# =====================================================
def classify_module(name: str):
    name_lower = name.lower()

    scores = {"SERVICE": 0, "TASK": 0, "HYBRID": 0}

    for t, rules in EXECUTION_TYPES.items():
        for kw in rules["keywords"]:
            if kw in name_lower:
                scores[t] += 1

    # HYBRID override logic
    if "orchestrator" in name_lower or "launcher" in name_lower:
        return "HYBRID"

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "TASK"

    return best


# =====================================================
# EXECUTION INTERPRETER
# =====================================================
def interpret_exit(module_name: str, log_text: str, exec_type: str):
    log_text = log_text.lower()

    # HARD FAILURE SIGNALS
    if "traceback" in log_text or "error" in log_text:
        return "CRASH"

    if "modulenotfounderror" in log_text:
        return "IMPORT_FAIL"

    # TYPE-AWARE LOGIC
    if exec_type == "SERVICE":
        if len(log_text.strip()) == 0:
            return "DOWN_SERVICE"
        return "RUNNING"

    if exec_type == "TASK":
        if len(log_text.strip()) == 0:
            return "TASK_NO_OUTPUT"
        return "TASK_COMPLETE"

    if exec_type == "HYBRID":
        return "MIXED_STATE"

    return "UNKNOWN"


# =====================================================
# LOG ANALYZER
# =====================================================
def analyze_runtime(name: str):
    log_path = LOGS / f"{name}.log"

    if not log_path.exists():
        return "NO_LOG", "UNKNOWN"

    try:
        data = log_path.read_text(errors="ignore")
    except Exception:
        return "READ_FAIL", "UNKNOWN"

    exec_type = classify_module(name)
    state = interpret_exit(name, data, exec_type)

    return state, exec_type


# =====================================================
# STACK REGISTRY (NO MORE GUESSING)
# =====================================================
def get_stack():
    return {
        "swarm_bus": "runtime_v7/core/v9_9_swarm_bus_v14.py",
        "memory": "omega_swarm_memory_bridge_v9.py",
        "assistant": "omega_unified_brain_v22.py",
        "emitter": "runtime_v7/core/test_swarm_emitter.py",
    }


# =====================================================
# MAIN DIAGNOSTIC ENGINE
# =====================================================
def run_registry():
    print("\n🧬 OMEGA EXECUTION TYPE REGISTRY V1\n")

    stack = get_stack()

    for name, path in stack.items():

        exec_type = classify_module(name)
        state, inferred_type = analyze_runtime(name)

        print("──────────────────────────────")
        print(f"MODULE   : {name}")
        print(f"PATH     : {path}")
        print(f"TYPE     : {exec_type}")
        print(f"STATE    : {state}")
        print(f"LOG TYPE : {inferred_type}")

    print("\n🧠 REGISTRY COMPLETE")


if __name__ == "__main__":
    run_registry()
