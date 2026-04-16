import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"


# =====================================================
# SYSTEM GRAPH (CAUSAL DEPENDENCIES)
# =====================================================
GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}


# =====================================================
# EXECUTION TYPE MODEL
# =====================================================
EXEC_TYPE = {
    "swarm_bus": "SERVICE",
    "memory": "TASK",
    "assistant": "SERVICE",
    "emitter": "TASK"
}


# =====================================================
# PROCESS CHECK
# =====================================================
def ps_snapshot():
    try:
        out = subprocess.check_output(["ps", "-A"], text=True)
        return out.lower().splitlines()
    except Exception:
        return []


def is_running(ps_lines, signature):
    for line in ps_lines:
        if signature in line:
            return True
    return False


# =====================================================
# SEMANTIC HEALTH SCORE
# =====================================================
def semantic_health(module):
    path = LOGS / f"{module}.log"
    if not path.exists():
        return 0.3

    data = path.read_text(errors="ignore").lower()

    score = 0.5

    if "heartbeat" in data or "alive" in data:
        score += 0.3
    if "error" in data or "traceback" in data:
        score -= 0.4
    if len(data.strip()) == 0:
        score -= 0.2

    return max(0.0, min(1.0, score))


# =====================================================
# BASE HEALTH
# =====================================================
def base_health(module, ps_lines):
    running = is_running(ps_lines, module)
    semantic = semantic_health(module)

    if running:
        return 0.6 + (semantic * 0.4)
    else:
        return 0.1 + (semantic * 0.3)


# =====================================================
# CAUSAL PROPAGATION ENGINE
# =====================================================
def propagate_health(base_scores):
    """
    Health flows DOWNSTREAM in dependency graph.
    """
    propagated = base_scores.copy()

    for parent, children in GRAPH.items():
        for child in children:
            if parent in propagated:
                influence = propagated[parent] * 0.25
                propagated[child] = min(
                    1.0,
                    propagated.get(child, 0) + influence
                )

    return propagated


# =====================================================
# CAUSAL RISK ENGINE
# =====================================================
def compute_risk(scores):
    risk_map = {}

    for module, score in scores.items():
        dependencies = [p for p, c in GRAPH.items() if module in c]

        dependency_risk = 0
        for d in dependencies:
            dependency_risk += (1 - scores.get(d, 0)) * 0.3

        total_risk = (1 - score) + dependency_risk
        risk_map[module] = min(1.0, total_risk)

    return risk_map


# =====================================================
# SYSTEM ENGINE
# =====================================================
def run_graph():
    ps_lines = ps_snapshot()

    modules = list(GRAPH.keys())

    base_scores = {}
    semantic_scores = {}

    print("\n🧠 OMEGA CAUSAL HEALTH GRAPH v1\n")

    # -----------------------------
    # BASE SCORING
    # -----------------------------
    for m in modules:
        base_scores[m] = base_health(m, ps_lines)

    # -----------------------------
    # PROPAGATION
    # -----------------------------
    propagated = propagate_health(base_scores)

    # -----------------------------
    # RISK CALCULATION
    # -----------------------------
    risks = compute_risk(propagated)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    for m in modules:
        print("──────────────────────────────")
        print(f"MODULE : {m}")
        print(f"BASE HEALTH       : {round(base_scores[m], 3)}")
        print(f"PROPAGATED HEALTH : {round(propagated[m], 3)}")
        print(f"CAUSAL RISK       : {round(risks[m], 3)}")

    # -----------------------------
    # SYSTEM SUMMARY
    # -----------------------------
    global_health = sum(propagated.values()) / len(propagated)
    max_risk = max(risks.values())

    print("\n══════════════════════════════")
    print(f"🧠 GLOBAL CAUSAL HEALTH: {round(global_health, 3)}")
    print(f"⚠️ MAX NODE RISK      : {round(max_risk, 3)}")

    if max_risk > 0.7:
        print("🔴 SYSTEM STATE: CASCADING FAILURE RISK")
    elif global_health > 0.75:
        print("🟢 SYSTEM STATE: STABLE CAUSAL GRAPH")
    else:
        print("🟡 SYSTEM STATE: DEGRADED BUT STABLE")

    print("══════════════════════════════\n")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_graph()
