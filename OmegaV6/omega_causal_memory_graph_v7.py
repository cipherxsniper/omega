import time
import random
from collections import defaultdict, deque

# =====================================================
# 🧠 CAUSAL GRAPH (BASE STRUCTURE)
# =====================================================
GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

NODES = list(GRAPH.keys())

# =====================================================
# 🧠 CAUSAL MEMORY (v7)
# =====================================================
memory = defaultdict(lambda: deque(maxlen=100))

# =====================================================
# 🧬 NODE STATE (v8 IDENTITY LAYER)
# =====================================================
state = defaultdict(lambda: {
    "health": 1.0,
    "risk": 0.0,
    "identity": {
        "stability": 0.5,
        "volatility": 0.5,
        "adaptability": 0.5
    }
})

# =====================================================
# 🧠 CAUSAL HISTORY WRITER
# =====================================================
def log_event(node, event, reason):
    memory[node].append({
        "event": event,
        "reason": reason,
        "time": time.time()
    })

# =====================================================
# 🧪 SIMULATED DYNAMICS (REAL SYSTEM WOULD REPLACE THIS)
# =====================================================
def drift(node):
    # volatility influenced by past instability
    v = state[node]["identity"]["volatility"]
    noise = random.uniform(-0.15, 0.1) * (1 + v)

    state[node]["health"] = max(
        0.0,
        min(1.0, state[node]["health"] + noise)
    )

# =====================================================
# 🧠 v8: IDENTITY LEARNING
# =====================================================
def update_identity(node):
    hist = list(memory[node])

    failures = len([h for h in hist if h["event"] == "FAILURE"])
    stable = len([h for h in hist if h["event"] == "STABLE"])

    total = max(1, len(hist))

    failure_ratio = failures / total
    stability_ratio = stable / total

    state[node]["identity"]["stability"] = stability_ratio
    state[node]["identity"]["volatility"] = failure_ratio

    # adaptability emerges from variance
    state[node]["identity"]["adaptability"] = abs(stability_ratio - failure_ratio)

# =====================================================
# 🧠 v9: CAUSAL GRAPH REWRITER
# =====================================================
def rewrite_graph():
    for node in NODES:
        iden = state[node]["identity"]

        # unstable nodes lose dependencies
        if iden["volatility"] > 0.6:
            GRAPH[node] = []

        # stable nodes gain observational edges
        if iden["stability"] > 0.7:
            for target in NODES:
                if target != node and target not in GRAPH[node]:
                    GRAPH[node].append(target)

# =====================================================
# 🧠 FAILURE ANALYSIS (CAUSAL)
# =====================================================
def analyze(node):
    hist = list(memory[node])

    if len(hist) < 3:
        return "INSUFFICIENT_DATA"

    last = hist[-3:]

    if all(h["event"] == "FAILURE" for h in last):
        return "RECURRING_COLLAPSE"

    if state[node]["health"] < 0.2:
        return "CRITICAL_DEGRADATION"

    return "NORMAL"

# =====================================================
# 🧠 v10: STABILIZATION ENGINE
# =====================================================
def stabilize(node):
    iden = state[node]["identity"]

    # damp volatility over time (prevents oscillation loops)
    iden["volatility"] *= 0.95

    # reinforce stable behavior
    if state[node]["health"] > 0.7:
        iden["stability"] = min(1.0, iden["stability"] + 0.02)

# =====================================================
# 🧠 NODE EVALUATION LOOP
# =====================================================
def evaluate(node):
    drift(node)
    update_identity(node)

    h = state[node]["health"]
    reason = analyze(node)

    if h < 0.25:
        log_event(node, "FAILURE", reason)
        return "FAILURE", reason

    elif h < 0.6:
        log_event(node, "DEGRADED", "LOW_HEALTH")
        return "DEGRADED", "LOW_HEALTH"

    else:
        log_event(node, "STABLE", "OK")
        return "STABLE", "OK"

# =====================================================
# 🧠 CAUSAL INSIGHT ENGINE
# =====================================================
def insight(node):
    hist = memory[node]
    reasons = defaultdict(int)

    for h in hist:
        reasons[h["reason"]] += 1

    if not reasons:
        return "NO_HISTORY"

    return max(reasons, key=reasons.get)

# =====================================================
# 🧠 MAIN LOOP (SELF-EVOLVING SYSTEM)
# =====================================================
def run():
    print("\n🧠 OMEGA CAUSAL MEMORY GRAPH v7 (EVOLVED CORE)\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        for node in NODES:
            status, reason = evaluate(node)
            stabilize(node)

            print("\n────────────────────────")
            print("NODE     :", node)
            print("STATUS   :", status)
            print("REASON   :", reason)
            print("INSIGHT  :", insight(node))

            iden = state[node]["identity"]
            print("HEALTH   :", round(state[node]["health"], 3))
            print("STABILITY:", round(iden["stability"], 3))
            print("VOLATILITY:", round(iden["volatility"], 3))

            if status == "FAILURE":
                print("🚨 CAUSAL EVENT: FAILURE RECORDED")
            elif status == "DEGRADED":
                print("⚠️ CAUSAL EVENT: DEGRADATION")
            else:
                print("🟢 CAUSAL EVENT: STABLE")

        rewrite_graph()

        print("\n════════════════════════════")
        print("🧠 SYSTEM EVOLVING CAUSALLY")
        print("GRAPH STATE:", GRAPH)
        print("════════════════════════════")

        time.sleep(5)


if __name__ == "__main__":
    run()
