import os
from pathlib import Path
import subprocess

OMEGA_ROOT = Path.home() / "Omega"
OMEGA_V6 = OMEGA_ROOT / "OmegaV6"
CORE_DIR = OMEGA_V6 / "runtime_v7" / "core"

LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


# -----------------------------
# SAFE FILE RESOLVER
# -----------------------------
def safe_find(patterns, grep=None, search_paths=None):
    search_paths = search_paths or [OMEGA_ROOT, OMEGA_V6, CORE_DIR]
    results = []

    for base in search_paths:
        for pattern in patterns:
            try:
                results.extend(base.rglob(pattern))
            except Exception:
                pass

    if grep and results:
        filtered = [
            r for r in results
            if any(tag in str(r) for tag in grep)
        ]
        if filtered:
            results = filtered

    results = sorted(set(results))
    return str(results[-1]) if results else None


# -----------------------------
# STACK RESOLVER (V10)
# -----------------------------
def resolve_stack_v10():
    swarm_bus = safe_find(
        ["*swarm_bus*.py", "*event_bus*.py", "*omega_bus*.py", "*bus*.py"],
        grep=["v14", "v15", "v16", "v17", "v13", "v12"],
        search_paths=[CORE_DIR, OMEGA_V6, OMEGA_ROOT]
    )

    if not swarm_bus:
        swarm_bus = safe_find(
            ["*swarm_bus*.py", "*bus*.py"],
            search_paths=[CORE_DIR, OMEGA_V6, OMEGA_ROOT]
        )

    memory = safe_find(
        ["omega_crdt_memory_v*.py", "omega_memory*.py", "*graph_memory*.py", "*memory*.py"],
        search_paths=[OMEGA_ROOT, OMEGA_V6, CORE_DIR]
    )

    assistant = safe_find(
        ["omega_assistant*.py", "omega_unified_brain*.py", "omega_*brain*.py", "omega_*generator*.py"],
        search_paths=[OMEGA_ROOT, OMEGA_V6, CORE_DIR]
    )

    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


# -----------------------------
# LAUNCH ENGINE
# -----------------------------
def launch(cmd):
    if not cmd:
        return False
    subprocess.Popen(cmd, shell=True)
    return True


def resolve_launch():
    stack = resolve_stack_v10()

    commands = {}

    if stack["swarm_bus"]:
        commands["swarm_bus"] = f"nohup python {stack['swarm_bus']} > logs/bus.log 2>&1 &"

    if stack["memory"]:
        commands["memory"] = f"nohup python {stack['memory']} > logs/memory.log 2>&1 &"

    if stack["assistant"]:
        commands["assistant"] = f"nohup python {stack['assistant']} > logs/assistant.log 2>&1 &"

    if stack["emitter"]:
        commands["emitter"] = f"nohup python {stack['emitter']} > logs/emitter.log 2>&1 &"

    print("\n🧠 OMEGA BOOT RESOLVER V10\n")

    print("📦 STACK:")
    for k, v in stack.items():
        print(f"  {k:10}: {v}")

    print("\n🚀 EXECUTING LAUNCH SEQUENCE...\n")

    for name, cmd in commands.items():
        print(f"[BOOT] {name}: {cmd}")
        launch(cmd)

    print("\n🟢 BOOT COMPLETE\n")
    for k in commands:
        print(f"  ✅ {k} launched")


if __name__ == "__main__":
    resolve_launch()
