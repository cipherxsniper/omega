import os
import re
from pathlib import Path

CORE_DIR = Path("runtime_v7/core")

# -----------------------------
# VERSION SCORING ENGINE
# -----------------------------
def score_version(path: str) -> int:
    if not path:
        return -1

    name = os.path.basename(path)

    # extract version numbers like v13, v14, v15...
    matches = re.findall(r"v(\d+)", name)

    if not matches:
        return 0

    # take highest version found in filename
    versions = [int(m) for m in matches]
    v = max(versions)

    # weight newer systems higher (bias toward 14+ as "modern swarm")
    if v >= 17:
        return v * 10 + 50
    if v >= 15:
        return v * 10 + 30
    if v >= 13:
        return v * 10 + 10
    return v * 10


# -----------------------------
# SAFE RESOLVER CORE
# -----------------------------
def resolve_latest(patterns, grep=None):
    candidates = []

    for pattern in patterns:
        for p in CORE_DIR.glob(pattern):
            if p.exists():
                candidates.append(str(p))

    # optional grep filter (version preference)
    if grep and candidates:
        filtered = []
        for c in candidates:
            if any(g in c for g in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    if not candidates:
        return None

    # rank by score
    candidates.sort(key=score_version, reverse=True)

    return candidates[0]


# -----------------------------
# MAIN STACK RESOLVER v2
# -----------------------------
def resolve_stack():
    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v14", "v15", "v16", "v17", "v13"]
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
        "omega_memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py"
    ])

    emitter = CORE_DIR / "test_swarm_emitter.py"
    emitter = str(emitter) if emitter.exists() else None

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


# -----------------------------
# BOOT TEST (SAFE DIAGNOSTIC)
# -----------------------------
if __name__ == "__main__":
    stack = resolve_stack()

    print("\n🧠 OMEGA BOOT RESOLVER v2")
    print("==========================")

    for k, v in stack.items():
        print(f"{k:10} -> {v}")

    if not stack["swarm_bus"]:
        print("\n[BOOT ERROR] swarm_bus not resolved")
    else:
        print("\n[OK] Boot stack resolved successfully")
