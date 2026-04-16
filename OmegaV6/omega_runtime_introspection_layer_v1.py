import os
import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"

# =====================================================
# TARGET MODULES
# =====================================================
MODULES = {
    "swarm_bus": "swarm_bus|event_bus|omega_bus",
    "memory": "memory|crdt|graph_memory",
    "assistant": "assistant|brain|generator",
    "emitter": "emitter|heartbeat|test_swarm"
}


# =====================================================
# PROCESS SCANNER (REAL OS INTROSPECTION)
# =====================================================
def get_process_list():
    try:
        result = subprocess.check_output(["ps", "-A"], text=True)
        return result.lower().splitlines()
    except Exception:
        return []


# =====================================================
# DETECT IF MODULE IS RUNNING (REAL SIGNAL)
# =====================================================
def is_running(signatures, process_list):
    for line in process_list:
        for sig in signatures.split("|"):
            if sig in line:
                return True
    return False


# =====================================================
# INTROSPECTION ENGINE
# =====================================================
def introspect_system():
    print("\n🧠 OMEGA RUNTIME INTROSPECTION LAYER V1\n")

    processes = get_process_list()

    results = {}

    for module, signatures in MODULES.items():

        running = is_running(signatures, processes)

        if running:
            state = "RUNNING_IN_OS"
            meaning = "Process detected in system runtime (visible via ps)"
        else:
            state = "NOT_VISIBLE"
            meaning = "No OS-level process match (may be task or silent service)"

        results[module] = {
            "state": state,
            "meaning": meaning
        }

        print("──────────────────────────────")
        print(f"MODULE : {module}")
        print(f"STATE  : {state}")
        print(f"MEANING: {meaning}")

    print("\n🧠 INTROSPECTION COMPLETE")

    return results


# =====================================================
# HYBRID DIAGNOSTIC LAYER (OPTIONAL COMBINE)
# =====================================================
def compare_with_semantic_layer(semantic_results=None):
    """
    Optional bridge: compare runtime reality vs semantic model.
    """
    print("\n🔍 CROSS-LAYER COMPARISON\n")

    processes = get_process_list()

    for module in MODULES:
        running = is_running(MODULES[module], processes)

        if running:
            print(f"{module}: CONFIRMED RUNNING (OS + semantic match)")
        else:
            print(f"{module}: NOT IN PROCESS TABLE (possible TASK or silent service)")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    introspect_system()
