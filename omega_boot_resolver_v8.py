import os
import re
from pathlib import Path
from glob import glob

OMEGA_ROOTS = [
    Path.home() / "Omega",
    Path.home() / "Omega/OmegaV6"
]

PRIORITY_VERSIONS = ["v17", "v16", "v15", "v14", "v13", "v12", "v11", "v10", "v9"]


def score_path(path: str) -> int:
    """Higher score = better version match"""
    score = 0
    for i, v in enumerate(PRIORITY_VERSIONS):
        if v in path:
            score += (len(PRIORITY_VERSIONS) - i) * 10
    return score


def deep_scan(patterns):
    results = []

    for root in OMEGA_ROOTS:
        for pattern in patterns:
            results.extend(glob(str(root / "**" / pattern), recursive=True))

    # filter valid files
    results = [r for r in results if os.path.exists(r)]
    return results


def resolve_latest(patterns, grep=None):
    candidates = deep_scan(patterns)

    if grep:
        filtered = []
        for c in candidates:
            if any(g in c for g in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    if not candidates:
        return None

    # rank by version + recency (filename order bias)
    candidates.sort(key=lambda x: (score_path(x), len(x)), reverse=True)
    return candidates[0]


def resolve_stack():
    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v17", "v16", "v15", "v14", "v13"]
    )

    if not swarm_bus:
        swarm_bus = resolve_latest([
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ])

    memory = resolve_latest([
        "omega_crdt_memory_v*.py",
        "omega_graph_memory*.py",
        "*memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py",
        "*brain*.py"
    ])

    emitter = resolve_latest([
        "test_swarm_emitter.py",
        "*emitter*.py"
    ])

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


if __name__ == "__main__":
    import json
    print("\n🧠 OMEGA BOOT RESOLVER V8\n")
    print(json.dumps(resolve_stack(), indent=2))
