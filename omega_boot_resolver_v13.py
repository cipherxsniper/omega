import os
import time
import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"
V6 = ROOT / "OmegaV6"
CORE = V6 / "runtime_v7" / "core"


# -----------------------------
# DEPENDENCY GRAPH (WORLD MODEL)
# -----------------------------
DEPENDENCIES = {
    "emitter": [],
    "swarm_bus": ["emitter"],
    "memory": ["swarm_bus"],
    "assistant": ["memory"]
}


# -----------------------------
# FIND FILE
# -----------------------------
def find(patterns):
    results = []

    for base in [ROOT, V6, CORE]:
        for p in patterns:
            try:
                results.extend(base.rglob(p))
            except:
                pass

    results = sorted(set(results))
    return str(results[-1]) if results else None


# -----------------------------
# WORLD MODEL VALIDATION
# -----------------------------
def can_boot(node, resolved):
    deps = DEPENDENCIES.get(node, [])

    for d in deps:
        if not resolved.get(d):
            return False, f"BLOCKED_BY_{d.upper()}"

    return True, "OK"


# -----------------------------
# RESOLVE STACK
# -----------------------------
def resolve():
    return {
        "emitter": str(CORE / "test_swarm_emitter.py"),
        "swarm_bus": find(["*swarm_bus*.py", "*event_bus*.py"]),
        "memory": find(["omega_*memory*.py", "*memory*.py"]),
        "assistant": find(["omega_*brain*.py", "omega_assistant*.py"])
    }


# -----------------------------
# LAUNCH
# -----------------------------
def launch(name, path):
    if not path:
        print(f"[BLOCKED] {name} missing file")
        return False

    print(f"[BOOT] {name}: {path}")
    subprocess.Popen(f"nohup python {path} > logs/{name}.log 2>&1 &", shell=True)
    return True


# -----------------------------
# BOOT SEQUENCE (ORDERED WORLD MODEL)
# -----------------------------
def boot():
    resolved = resolve()

    print("\n🧠 V13 WORLD MODEL BOOT ENGINE\n")

    # enforce dependency order
    order = ["emitter", "swarm_bus", "memory", "assistant"]

    for node in order:
        ok, reason = can_boot(node, resolved)

        if not ok:
            print(f"[WORLD BLOCK] {node} → {reason}")
            continue

        launch(node, resolved[node])


# -----------------------------
# CONTINUOUS VALIDATION
# -----------------------------
def monitor():
    while True:
        resolved = resolve()

        for node in ["swarm_bus", "memory", "assistant"]:
            if not resolved[node]:
                print(f"[FAULT] {node} missing in world model")

        time.sleep(10)


if __name__ == "__main__":
    boot()
    monitor()
