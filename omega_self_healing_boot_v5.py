import os
import glob
import time
from pathlib import Path

CORE_DIR = Path("runtime_v7/core")


def resolve_latest(patterns, grep=None):
    """
    Finds latest versioned file safely.
    """
    candidates = []

    for pattern in patterns:
        candidates.extend(glob.glob(str(CORE_DIR / pattern)))

    if not candidates:
        return None

    # optional filtering (v13+ priority system)
    if grep:
        filtered = []
        for c in candidates:
            if any(g in c for g in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    return sorted(candidates)[-1]


def resolve_stack():
    print("\n🧠 [OMEGA V5 SELF-HEALING RESOLVER]\n")

    # ----------------------------
    # PASS 1 — INTELLIGENT MATCH
    # ----------------------------
    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v13", "v14", "v15", "v16", "v17"]
    )

    memory = resolve_latest([
        "omega_crdt_memory_v*.py",
        "omega_memory*.py",
        "omega_shared_memory*.py",
        "omega_graph_memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py",
        "omega_chat*.py"
    ])

    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    # ----------------------------
    # PASS 2 — BROAD FALLBACK HEAL
    # ----------------------------
    if not swarm_bus:
        print("[HEAL] Swarm bus missing → running deep scan...")
        swarm_bus = resolve_latest(["*.py"], grep=["swarm_bus", "bus", "event_bus"])

    if not memory:
        print("[HEAL] Memory missing → fallback scan...")
        memory = resolve_latest(["*.py"], grep=["memory", "crdt", "graph"])

    if not assistant:
        print("[HEAL] Assistant missing → fallback scan...")
        assistant = resolve_latest(["*.py"], grep=["assistant", "chat", "omega"])

    # ----------------------------
    # PASS 3 — VALIDATION LAYER
    # ----------------------------
    missing = []

    if not swarm_bus:
        missing.append("swarm_bus")
    if not memory:
        missing.append("memory")
    if not assistant:
        missing.append("assistant")

    if missing:
        print("\n❌ [BOOT FAILED - UNHEALED COMPONENTS]")
        for m in missing:
            print("   -", m)
        return None

    stack = {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }

    print("\n🟢 [OMEGA V5 STACK READY]")
    for k, v in stack.items():
        print(f"   {k}: {v}")

    return stack


if __name__ == "__main__":
    resolve_stack()
