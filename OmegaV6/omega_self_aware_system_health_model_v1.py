import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"


# =====================================================
# CORE MODULE REGISTRY
# =====================================================
MODULES = {
    "swarm_bus": "swarm_bus|event_bus|omega_bus",
    "memory": "memory|crdt|graph_memory",
    "assistant": "assistant|brain|generator",
    "emitter": "emitter|heartbeat|test_swarm"
}


# =====================================================
# EXECUTION TYPE MODEL
# =====================================================
EXECUTION_TYPE = {
    "swarm_bus": "SERVICE",
    "memory": "TASK",
    "assistant": "SERVICE",
    "emitter": "TASK"
}


# =====================================================
# PROCESS INTROSPECTION
# =====================================================
def ps_snapshot():
    try:
        out = subprocess.check_output(["ps", "-A"], text=True)
        return out.lower().splitlines()
    except Exception:
        return []


def is_running(lines, sigs):
    for line in lines:
        for s in sigs.split("|"):
            if s in line:
                return True
    return False


# =====================================================
# SEMANTIC SIGNAL SCORING
# =====================================================
def semantic_score(module):
    path = LOGS / f"{module}.log"
    if not path.exists():
        return 0.2  # partial ignorance

    data = path.read_text(errors="ignore").lower()

    score = 0.5  # neutral baseline

    if "heartbeat" in data:
        score += 0.3
    if "error" in data or "traceback" in data:
        score -= 0.4
    if "alive" in data:
        score += 0.2
    if len(data.strip()) == 0:
        score -= 0.2

    return max(0.0, min(1.0, score))


# =====================================================
# HEALTH ENGINE CORE
# =====================================================
def evaluate_module(module, ps_lines):
    runtime = is_running(ps_lines, MODULES[module])
    semantic = semantic_score(module)
    exec_type = EXECUTION_TYPE[module]

    # =========================
    # HEALTH COMPUTATION
    # =========================
    health = 0.0

    # Runtime contribution
    if runtime:
        health += 0.5
    else:
        health += 0.1 if exec_type == "TASK" else 0.0

    # Semantic contribution
    health += semantic * 0.5

    # Execution alignment bonus
    if exec_type == "SERVICE" and runtime:
        health += 0.2
    if exec_type == "TASK" and not runtime:
        health += 0.1

    health = max(0.0, min(1.0, health))

    # =========================
    # STATE CLASSIFICATION
    # =========================
    if health > 0.85:
        state = "OPTIMAL"
    elif health > 0.65:
        state = "STABLE"
    elif health > 0.4:
        state = "DEGRADED"
    else:
        state = "CRITICAL"

    return {
        "module": module,
        "execution_type": exec_type,
        "runtime": runtime,
        "semantic_score": round(semantic, 3),
        "health": round(health, 3),
        "state": state
    }


# =====================================================
# GLOBAL SYSTEM HEALTH (SELF-AWARENESS CORE)
# =====================================================
def system_health_report():
    ps_lines = ps_snapshot()

    results = []

    print("\n🧠 OMEGA SELF-AWARE SYSTEM HEALTH MODEL v1\n")

    total_health = 0

    for m in MODULES:
        r = evaluate_module(m, ps_lines)
        results.append(r)
        total_health += r["health"]

        print("──────────────────────────────")
        print(f"MODULE : {r['module']}")
        print(f"TYPE   : {r['execution_type']}")
        print(f"RUNTIME: {r['runtime']}")
        print(f"SEMANTIC SCORE: {r['semantic_score']}")
        print(f"HEALTH : {r['health']}")
        print(f"STATE  : {r['state']}")

    global_health = total_health / len(MODULES)

    print("\n══════════════════════════════")
    print(f"🧠 GLOBAL SYSTEM HEALTH: {round(global_health, 3)}")

    if global_health > 0.85:
        print("🟢 SYSTEM STATUS: OPTIMAL")
    elif global_health > 0.65:
        print("🟡 SYSTEM STATUS: STABLE")
    elif global_health > 0.4:
        print("🟠 SYSTEM STATUS: DEGRADED")
    else:
        print("🔴 SYSTEM STATUS: CRITICAL")

    print("══════════════════════════════\n")

    return {
        "global_health": global_health,
        "modules": results
    }


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    system_health_report()
