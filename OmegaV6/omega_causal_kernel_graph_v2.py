import time
from collections import defaultdict, deque
from pathlib import Path

# =========================
# SYSTEM GRAPH (CAUSAL MAP)
# =========================
GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

NODES = list(GRAPH.keys())

# =========================
# STATE MEMORY
# =========================
history = defaultdict(lambda: deque(maxlen=5))

# =========================
# MOCK HEALTH SIGNAL (replace with real runtime hooks later)
# =========================
def get_health(module):
    # simulate based on simple rule (extend later with ps/log hooks)
    return 0.2 if module in ["swarm_bus", "memory"] else 0.8

# =========================
# TREND ENGINE
# =========================
def trend(values):
    if len(values) < 3:
        return "UNKNOWN"
    if values[-1] < values[-2] < values[-3]:
        return "DECLINING"
    if values[-1] > values[-2] > values[-3]:
        return "IMPROVING"
    return "STABLE"

# =========================
# CAUSAL PRESSURE MODEL
# =========================
def downstream_impact(module, risk_map):
    impact = 0.0
    for parent, children in GRAPH.items():
        if module in children:
            impact += risk_map.get(parent, 0) * 0.5
    return impact

def upstream_dependency_risk(module, risk_map):
    return risk_map.get(module, 0)

# =========================
# COLLAPSE SCORE ENGINE
# =========================
def collapse_score(module, risk_map):
    base = upstream_dependency_risk(module, risk_map)
    pressure = downstream_impact(module, risk_map)

    return min(1.0, base + pressure)

# =========================
# UPDATE HISTORY
# =========================
def update(module, value):
    history[module].append(value)

# =========================
# CAUSAL GRAPH ANALYSIS LOOP
# =========================
def run():
    print("\n🧠 OMEGA CAUSAL KERNEL GRAPH v2\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        risk_map = {}
        collapse_map = {}

        # STEP 1: HEALTH COLLECTION
        for m in NODES:
            h = get_health(m)
            update(m, h)
            risk_map[m] = 1.0 - h

        # STEP 2: CAUSAL COLLAPSE COMPUTATION
        for m in NODES:
            collapse_map[m] = collapse_score(m, risk_map)

        # STEP 3: OUTPUT GRAPH STATE
        for m in NODES:
            print("\n────────────────────────")
            print(f"NODE      : {m}")
            print(f"HEALTH    : {round(1 - risk_map[m], 3)}")
            print(f"RISK      : {round(risk_map[m], 3)}")
            print(f"COLLAPSE  : {round(collapse_map[m], 3)}")
            print(f"TREND     : {trend(history[m])}")

            if collapse_map[m] > 0.75:
                print("🚨 STATE: CRITICAL CASCADE RISK")
            elif collapse_map[m] > 0.5:
                print("⚠️ STATE: CAUSAL INSTABILITY")
            else:
                print("🟢 STATE: STABLE")

        # STEP 4: SYSTEM SUMMARY
        system_score = sum(collapse_map.values()) / len(collapse_map)

        print("\n════════════════════════════")
        print(f"🧠 SYSTEM CASCADING RISK: {round(system_score, 3)}")

        if system_score > 0.7:
            print("🔴 SYSTEM STATE: CASCADING FAILURE RISK")
        elif system_score > 0.4:
            print("🟠 SYSTEM STATE: DEGRADED GRAPH")
        else:
            print("🟢 SYSTEM STATE: STABLE GRAPH")

        print("════════════════════════════")

        time.sleep(10)

if __name__ == "__main__":
    run()
