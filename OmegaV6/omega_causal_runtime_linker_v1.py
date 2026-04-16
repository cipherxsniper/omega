import os
import time
import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"
V6 = ROOT / "OmegaV6"
CORE = V6 / "runtime_v7" / "core"
LOGS = ROOT / "logs"

LOGS.mkdir(exist_ok=True)


# =====================================================
# RUNTIME NODE MODEL
# =====================================================
class RuntimeNode:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.last_seen = None
        self.heartbeat_count = 0
        self.status = "UNKNOWN"


# =====================================================
# LAUNCH PROCESS
# =====================================================
def launch(name, path):
    if not path:
        print(f"[BLOCKED] {name} not found")
        return None

    print(f"[LINKER BOOT] {name} → {path}")

    subprocess.Popen(
        f"nohup python {path} > logs/{name}.log 2>&1 &",
        shell=True
    )

    return RuntimeNode(name, path)


# =====================================================
# LIVE SIGNAL VERIFICATION (CORE IDEA)
# =====================================================
def check_alive(node: RuntimeNode):
    log_path = LOGS / f"{node.name}.log"

    if not log_path.exists():
        node.status = "NO_SIGNAL"
        return False

    try:
        data = log_path.read_text(errors="ignore")

        if len(data.strip()) == 0:
            node.status = "SILENT_EXIT"
            return False

        if "Traceback" in data:
            node.status = "CRASH"
            return False

        if "ModuleNotFoundError" in data:
            node.status = "IMPORT_FAIL"
            return False

        # heartbeat-style inference
        if "EVENT" in data or "heartbeat" in data:
            node.heartbeat_count += 1

        node.last_seen = time.time()
        node.status = "ALIVE"

        return True

    except Exception as e:
        node.status = f"READ_FAIL:{e}"
        return False


# =====================================================
# CAUSAL SCORE ENGINE
# =====================================================
def causal_score(node: RuntimeNode):
    if node.status != "ALIVE":
        return 0

    age = time.time() - (node.last_seen or time.time())

    score = node.heartbeat_count * 2

    if age < 5:
        score += 5

    return score


# =====================================================
# STACK LINKER (NOT FILE FINDER)
# =====================================================
def link_stack():
    return {
        "emitter": str(CORE / "test_swarm_emitter.py"),
        "swarm_bus": str(CORE / "v9_9_swarm_bus_v14.py"),
        "memory": str(ROOT / "omega_swarm_memory_bridge_v9.py"),
        "assistant": str(ROOT / "omega_unified_brain_v22.py"),
    }


# =====================================================
# BOOT SEQUENCE
# =====================================================
def boot():
    print("\n🧠 OMEGA CAUSAL RUNTIME LINKER V1\n")

    stack = link_stack()

    nodes = []

    for name, path in stack.items():
        node = launch(name, path)
        if node:
            nodes.append(node)

    time.sleep(3)
    return nodes


# =====================================================
# LIVING SYSTEM VERIFICATION LOOP
# =====================================================
def verify_loop(nodes):
    print("\n🛡️ CAUSAL VERIFICATION ACTIVE\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n────────── CYCLE {cycle} ──────────")

        active = 0

        for node in nodes:
            alive = check_alive(node)
            score = causal_score(node)

            status = "🟢" if alive else "🔴"

            print(f"{status} {node.name:10} | {node.status:12} | score={score}")

            if alive:
                active += 1

        print(f"\n📊 ACTIVE NODES: {active}/{len(nodes)}")

        # causal system health rule
        if active == 0:
            print("\n❌ SYSTEM DEADLOCK DETECTED — NO LIVING NODES")
        elif active < len(nodes) // 2:
            print("\n⚠️ DEGRADED SYSTEM STATE")

        time.sleep(10)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    nodes = boot()
    verify_loop(nodes)
