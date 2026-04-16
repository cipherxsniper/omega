import os
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"
OMEGA_V6 = OMEGA_ROOT / "OmegaV6"
CORE_DIR = OMEGA_V6 / "runtime_v7" / "core"


def safe_find(patterns, grep=None, search_paths=None):
    search_paths = search_paths or [OMEGA_ROOT, OMEGA_V6, CORE_DIR]

    results = []

    for base in search_paths:
        for pattern in patterns:
            try:
                found = list(base.rglob(pattern))
                results.extend(found)
            except Exception:
                pass

    if grep and results:
        filtered = []
        for r in results:
            if any(tag in str(r) for tag in grep):
                filtered.append(r)
        if filtered:
            results = filtered

    results = sorted(set(results))
    return str(results[-1]) if results else None


def resolve_stack_v9():
    swarm_bus = safe_find(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v14", "v15", "v16", "v17", "v13", "v12", "v11"],
        search_paths=[CORE_DIR, OMEGA_V6, OMEGA_ROOT]
    )

    if not swarm_bus:
        swarm_bus = safe_find(
            ["*swarm_bus*.py", "*omega_bus*.py", "*bus*.py"],
            search_paths=[CORE_DIR, OMEGA_V6, OMEGA_ROOT]
        )

    memory = safe_find(
        [
            "omega_crdt_memory_v*.py",
            "omega_memory*.py",
            "*graph_memory*.py",
            "*memory*.py"
        ],
        search_paths=[OMEGA_ROOT, OMEGA_V6, CORE_DIR]
    )

    assistant = safe_find(
        [
            "omega_assistant*.py",
            "omega_autonomous_brain*.py",
            "omega_*brain*.py",
            "omega_*generator*.py"
        ],
        grep=["v"],
        search_paths=[CORE_DIR, OMEGA_V6, OMEGA_ROOT]
    )

    emitter = safe_find(
        ["test_swarm_emitter.py", "*emitter*.py"],
        search_paths=[CORE_DIR, OMEGA_V6]
    )

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


def resolve_launch_commands():
    stack = resolve_stack_v9()
    commands = {}

    if stack["swarm_bus"]:
        commands["swarm_bus"] = f"nohup python {stack['swarm_bus']} > logs/bus.log 2>&1 &"

    if stack["memory"]:
        commands["memory"] = f"nohup python {stack['memory']} > logs/memory.log 2>&1 &"

    if stack["assistant"]:
        commands["assistant"] = f"nohup python {stack['assistant']} > logs/assistant.log 2>&1 &"

    if stack["emitter"]:
        commands["emitter"] = f"nohup python {stack['emitter']} > logs/emitter.log 2>&1 &"

    return stack, commands


if __name__ == "__main__":
    stack, cmds = resolve_launch_commands()

    print("\n🧠 OMEGA BOOT RESOLVER V9\n")

    print("📦 RESOLVED STACK:")
    for k, v in stack.items():
        print(f"  {k:10}: {v}")

    print("\n🚀 LAUNCH COMMANDS:")
    for k, v in cmds.items():
        print(f"  {k}: {v}")

    if not cmds:
        print("\n❌ SYSTEM INCOMPLETE - NOTHING TO LAUNCH")
