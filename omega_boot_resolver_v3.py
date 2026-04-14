import os
import glob
from pathlib import Path

CORE_DIR = Path("runtime_v7/core")


def resolve_latest(patterns, grep=None):
    """
    Finds newest matching file using version sorting.
    Optional grep filter narrows candidates by keyword.
    """

    candidates = []

    for pattern in patterns:
        candidates.extend(glob.glob(str(CORE_DIR / pattern)))

    if not candidates:
        return None

    # optional grep filter (version tags)
    if grep:
        filtered = []
        for c in candidates:
            if any(g in c for g in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    # sort by version-aware ordering
    candidates = sorted(candidates)

    return candidates[-1] if candidates else None


def resolve_stack():
    """
    OMEGA BOOT RESOLVER V2
    - strict fallback chain
    - multi-bus support
    - safe memory + assistant detection
    """

    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v14", "v15", "v16", "v17", "v13"]
    )

    # fallback if no "advanced versions" found
    if not swarm_bus:
        swarm_bus = resolve_latest([
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ])

    memory = resolve_latest([
        "omega_crdt_memory_v*.py",
        "omega_memory*.py",
        "omega_global_memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py"
    ])

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
