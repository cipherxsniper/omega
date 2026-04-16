import glob
from pathlib import Path

ROOT_DIR = Path(".")
CORE_DIR = Path("runtime_v7/core")


def find_all(patterns, roots):
    results = []
    for root in roots:
        for pattern in patterns:
            results.extend(glob.glob(str(root / pattern)))
    return results


def pick_best(files):
    if not files:
        return None
    return sorted(files)[-1]


def resolve_stack():
    """
    OMEGA BOOT RESOLVER V4 — REALITY-AWARE STACK ENGINE
    Fixes false nulls by accepting ecosystem equivalence
    """

    search_roots = [ROOT_DIR, CORE_DIR]

    # =====================================================
    # SWARM BUS (REAL ECOSYSTEM PRIORITY MAP)
    # =====================================================
    swarm_candidates = find_all([
        "*swarm_bus*.py",
        "*event_bus*.py",
        "omega_event_bus*.py",
        "omega_bus*.py",
        "omega_swarm_network*.py",
        "omega_cluster*.py",
        "omega_router*.py",
        "omega_network*.py",
    ], search_roots)

    # PRIORITY: event_bus > swarm_bus > omega_bus > others
    priority_order = [
        "event_bus",
        "swarm_bus",
        "omega_bus",
        "swarm_network",
        "router",
        "cluster"
    ]

    swarm_bus = None
    for p in priority_order:
        filtered = [f for f in swarm_candidates if p in f]
        if filtered:
            swarm_bus = pick_best(filtered)
            break

    if not swarm_bus:
        swarm_bus = pick_best(swarm_candidates)

    # =====================================================
    # MEMORY LAYER (ANY MEMORY SYSTEM VALID)
    # =====================================================
    memory_candidates = find_all([
        "*memory*.py",
        "*crdt*.py",
        "*graph*.py",
        "*state*.py",
        "*recursion*.py"
    ], search_roots)

    memory = pick_best(memory_candidates)

    # =====================================================
    # ASSISTANT LAYER (ANY INTELLIGENCE NODE)
    # =====================================================
    assistant_candidates = find_all([
        "*assistant*.py",
        "*brain*.py",
        "*intelligence*.py",
        "*chat*.py",
        "*cognition*.py"
    ], search_roots)

    assistant = pick_best(assistant_candidates)

    # =====================================================
    # EMITTER (STATIC SAFE NODE)
    # =====================================================
    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


if __name__ == "__main__":
    import json
    print(json.dumps(resolve_stack(), indent=2))
