import os
import subprocess
import time
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"

CORE_DIR = OMEGA_ROOT / "runtime_v7/core"
LOG_DIR = OMEGA_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)


# =====================================================
# UTILITY: RUN SHELL SAFE
# =====================================================
def run(cmd):
    return subprocess.getoutput(cmd)


# =====================================================
# RESOLVE LATEST FILE (SAFE + FLEXIBLE)
# =====================================================
def resolve_latest(patterns, grep=None):
    files = []

    for pattern in patterns:
        cmd = f"find {CORE_DIR} -name '{pattern}' 2>/dev/null"
        output = run(cmd).splitlines()
        files.extend(output)

    if not files:
        return None

    files = sorted(files)

    if grep:
        filtered = [f for f in files if any(g in f for g in grep)]
        if filtered:
            files = filtered

    return files[-1]


# =====================================================
# COMPONENT RESOLUTION
# =====================================================
def resolve_stack():
    swarm_bus = resolve_latest(
        ["*swarm_bus*.py"],
        grep=["v14", "v15", "v16", "v17", "v13"]
    )

    if not swarm_bus:
        swarm_bus = resolve_latest(["*swarm_bus*.py"])

    memory = resolve_latest(["omega_crdt_memory_v*.py"])

    assistant = resolve_latest(["omega_assistant*.py", "omega_*assistant*.py"])

    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


# =====================================================
# VALIDATION LAYER (CRITICAL)
# =====================================================
def validate(stack):
    for k, v in stack.items():
        if k == "memory":
            continue  # memory optional
        if not v or not os.path.exists(v):
            print(f"[BOOT RESOLVER][ERROR] Missing critical component: {k} → {v}")
            return False
    return True


# =====================================================
# LAUNCH SYSTEM
# =====================================================
def launch(stack):
    print("\n🧠⚙️ OMEGA BOOT RESOLVER v1")
    print("====================================")

    if stack["memory"]:
        print(f"[BOOT] Memory   : {stack['memory']}")
        subprocess.Popen(f"nohup python {stack['memory']} > logs/memory.log 2>&1 &", shell=True)

    print(f"[BOOT] Swarm    : {stack['swarm_bus']}")
    subprocess.Popen(f"nohup python {stack['swarm_bus']} > logs/bus.log 2>&1 &", shell=True)

    time.sleep(1)

    print(f"[BOOT] Emitter  : {stack['emitter']}")
    subprocess.Popen(f"nohup python {stack['emitter']} > logs/emitter.log 2>&1 &", shell=True)

    if stack["assistant"]:
        print(f"[BOOT] Assistant: {stack['assistant']}")
        subprocess.Popen(f"nohup python {stack['assistant']} > logs/assistant.log 2>&1 &", shell=True)

    print("\n🟢 OMEGA BOOT RESOLVER ONLINE")
    print("====================================\n")

    while True:
        time.sleep(10)
        print("[BOOT RESOLVER] system alive...")


# =====================================================
# ENTRYPOINT
# =====================================================
if __name__ == "__main__":
    stack = resolve_stack()

    if not validate(stack):
        print("[BOOT RESOLVER] FAILED SAFE VALIDATION → ABORT")
        exit(1)

    launch(stack)
