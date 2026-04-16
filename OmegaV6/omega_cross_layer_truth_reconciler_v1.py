import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"


# =====================================================
# LAYERS INPUT CONTRACTS (EXPECTED STRUCTURE)
# =====================================================

# These are optional imports from your existing systems
# If missing, system still works with partial truth


# =====================================================
# RUNTIME INTROSPECTION (REALITY LAYER)
# =====================================================
def get_process_list():
    try:
        out = subprocess.check_output(["ps", "-A"], text=True)
        return out.lower().splitlines()
    except Exception:
        return []


def is_running(processes, signatures):
    for line in processes:
        for sig in signatures:
            if sig in line:
                return True
    return False


# =====================================================
# SEMANTIC LAYER (MEANING LAYER - SIMPLIFIED INTERFACE)
# =====================================================
def get_semantic_state(module):
    """
    Pulls meaning from logs (if available).
    """
    path = LOGS / f"{module}.log"
    if not path.exists():
        return "NO_SEMANTIC_DATA"

    data = path.read_text(errors="ignore").lower()

    if "traceback" in data or "error" in data:
        return "FAILED"
    if "heartbeat" in data or "alive" in data:
        return "RUNNING"
    if len(data.strip()) == 0:
        return "COMPLETED"
    return "UNKNOWN"


# =====================================================
# EXECUTION TYPE LAYER (YOUR REGISTRY MODEL)
# =====================================================
EXECUTION_TYPES = {
    "swarm_bus": "SERVICE",
    "memory": "TASK",
    "assistant": "SERVICE",
    "emitter": "TASK"
}


# =====================================================
# RUNTIME SIGNATURES
# =====================================================
RUNTIME_SIGNATURES = {
    "swarm_bus": ["swarm_bus", "event_bus", "omega_bus"],
    "memory": ["memory", "crdt", "graph_memory"],
    "assistant": ["assistant", "brain", "generator"],
    "emitter": ["emitter", "heartbeat", "test_swarm"]
}


# =====================================================
# TRUTH ENGINE (CORE FUSION LAYER)
# =====================================================
def reconcile(module, processes):
    semantic = get_semantic_state(module)
    runtime = is_running(processes, RUNTIME_SIGNATURES[module])
    exec_type = EXECUTION_TYPES.get(module, "UNKNOWN")

    # ================================
    # TRUTH RULES ENGINE
    # ================================

    if runtime and semantic == "RUNNING":
        truth = "FULLY_ACTIVE"
        meaning = "Module is running and producing observable behavior"

    elif runtime and semantic == "NO_SEMANTIC_DATA":
        truth = "SILENT_RUNTIME"
        meaning = "Process exists but produces no log signals"

    elif not runtime and semantic == "COMPLETED":
        truth = "TASK_COMPLETE"
        meaning = "Task finished and exited cleanly"

    elif not runtime and semantic == "FAILED":
        truth = "CRASHED_TERMINATION"
        meaning = "Process failed and exited abnormally"

    elif not runtime and exec_type == "SERVICE":
        truth = "INVISIBLE_SERVICE"
        meaning = "Service not visible in OS but expected to persist"

    elif not runtime and exec_type == "TASK":
        truth = "TASK_COMPLETE"
        meaning = "Task likely executed and exited"

    else:
        truth = "UNKNOWN_STATE"
        meaning = "Cannot reconcile across layers"

    return {
        "module": module,
        "execution_type": exec_type,
        "semantic": semantic,
        "runtime": runtime,
        "truth": truth,
        "meaning": meaning
    }


# =====================================================
# SYSTEM EXECUTION
# =====================================================
def run_reconciler():
    modules = ["swarm_bus", "memory", "assistant", "emitter"]
    processes = get_process_list()

    print("\n🧠 OMEGA CROSS-LAYER TRUTH RECONCILER V1\n")

    results = []

    for m in modules:
        result = reconcile(m, processes)
        results.append(result)

        print("──────────────────────────────")
        print(f"MODULE : {result['module']}")
        print(f"TYPE   : {result['execution_type']}")
        print(f"SEMANTIC: {result['semantic']}")
        print(f"RUNTIME : {result['runtime']}")
        print(f"TRUTH   : {result['truth']}")
        print(f"MEANING : {result['meaning']}")

    print("\n🧠 TRUTH RECONCILIATION COMPLETE")

    return results


if __name__ == "__main__":
    run_reconciler()
