import os
import re
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"


def score_path(path: str):
    score = 0

    # version boost
    version_match = re.findall(r"v(\d+)", path)
    if version_match:
        score += int(version_match[-1]) * 10

    # priority boosts
    if "swarm_bus" in path:
        score += 100
    if "event_bus" in path:
        score += 80
    if "omega_bus" in path:
        score += 60
    if "assistant" in path:
        score += 50
    if "memory" in path:
        score += 70

    return score


def find_all(patterns):
    results = []
    for root, _, files in os.walk(OMEGA_ROOT):
        for f in files:
            for p in patterns:
                if re.fullmatch(p.replace("*", ".*"), f):
                    results.append(str(Path(root) / f))
    return results


def resolve_latest(patterns, grep=None):
    candidates = find_all(patterns)

    if grep:
        filtered = []
        for c in candidates:
            if any(g in c for g in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    if not candidates:
        return None

    ranked = sorted(candidates, key=score_path, reverse=True)
    return ranked[0]


def resolve_stack():
    print("\n🧠 [OMEGA BOOT RESOLVER V7] REALITY-AWARE SCAN STARTED\n")

    swarm_bus = resolve_latest(
        ["*swarm_bus*.py", "*event_bus*.py", "*omega_bus*.py", "*bus*.py"],
        grep=["v14", "v15", "v16", "v17", "v13"]
    )

    if not swarm_bus:
        swarm_bus = resolve_latest(
            ["*swarm_bus*.py", "*event_bus*.py", "*omega_bus*.py", "*bus*.py"]
        )

    memory = resolve_latest([
        "*crdt_memory*.py",
        "*memory*.py"
    ])

    assistant = resolve_latest([
        "*assistant*.py"
    ])

    emitter = resolve_latest([
        "*emitter*.py"
    ])

    print("\n📦 RESOLVED STACK (V7)")
    print(" swarm_bus :", swarm_bus)
    print(" memory    :", memory)
    print(" assistant :", assistant)
    print(" emitter   :", emitter)

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


if __name__ == "__main__":
    resolve_stack()
