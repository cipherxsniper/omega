import time
from collections import defaultdict

# =========================
# CAUSAL GRAPH (mutable)
# =========================
GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

NODES = list(GRAPH.keys())

# =========================
# STATE TRACKING
# =========================
state = defaultdict(lambda: {
    "health": 1.0,
    "risk": 0.0,
    "failures": 0,
    "isolated": False
})

# =========================
# HEALTH SIMULATION
# =========================
def probe(node):
    # Replace later with real runtime hooks
    if node in ["swarm_bus", "memory"]:
        return 0.25
    return 0.85

# =========================
# CASCADING RISK
# =========================
def compute_risk(node):
    return 1.0 - state[node]["health"]

# =========================
# DOWNSTREAM IMPACT
# =========================
def downstream_pressure(node):
    pressure = 0.0
    for parent, children in GRAPH.items():
        if node in children:
            pressure += state[parent]["risk"] * 0.5
    return pressure

# =========================
# REPAIR ENGINE
# =========================
def repair(node):
    s = state[node]

    # FAILURE DETECTION
    if s["health"] < 0.4:
        s["failures"] += 1

    # ISOLATION RULE
    if s["failures"] >= 2:
        s["isolated"] = True
        print(f"🧬 ISOLATING NODE: {node}")

        # remove from graph
        for parent in GRAPH:
            if node in GRAPH[parent]:
                GRAPH[parent].remove(node)

    # HEALING RULE
    if s["health"] < 0.6 and not s["isolated"]:
        s["health"] += 0.1  # soft recovery attempt

# =========================
# GRAPH REWIRING
# =========================
def reroute():
    # ensure assistant always reachable indirectly
    if state["assistant"]["isolated"]:
        print("⚠️ assistant isolated → injecting fallback path")
        if "memory" not in GRAPH["swarm_bus"]:
            GRAPH["swarm_bus"].append("assistant")

# =========================
# MAIN LOOP
# =========================
def run():
    print("\n🧠 OMEGA CAUSAL REPAIR ENGINE v3\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        # STEP 1: UPDATE HEALTH
        for n in NODES:
            state[n]["health"] = probe(n)
            state[n]["risk"] = compute_risk(n)

        # STEP 2: REPAIR PHASE
        for n in NODES:
            repair(n)

        # STEP 3: REWIRE GRAPH IF NEEDED
        reroute()

        # STEP 4: OUTPUT STATE
        total_risk = 0.0

        for n in NODES:
            s = state[n]
            pressure = downstream_pressure(n)

            score = min(1.0, s["risk"] + pressure)
            total_risk += score

            print("\n────────────────────────")
            print(f"NODE      : {n}")
            print(f"HEALTH    : {round(s['health'], 3)}")
            print(f"RISK      : {round(s['risk'], 3)}")
            print(f"PRESSURE  : {round(pressure, 3)}")
            print(f"ISOLATED  : {s['isolated']}")
            print(f"FAILURES  : {s['failures']}")
            print(f"FINAL     : {round(score, 3)}")

            if s["isolated"]:
                print("⛔ NODE IS ISOLATED")

        avg_risk = total_risk / len(NODES)

        print("\n════════════════════════════")
        print(f"🧠 SYSTEM RISK: {round(avg_risk, 3)}")

        if avg_risk > 0.7:
            print("🔴 SYSTEM STATE: UNSTABLE CASCADE")
        elif avg_risk > 0.4:
            print("🟠 SYSTEM STATE: DEGRADED")
        else:
            print("🟢 SYSTEM STATE: STABLE")

        print("════════════════════════════")

        time.sleep(10)

if __name__ == "__main__":
    run()
