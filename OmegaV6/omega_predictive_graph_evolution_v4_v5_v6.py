import time
import random
from collections import defaultdict

# =========================
# INITIAL CAUSAL GRAPH
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
state = defaultdict(lambda: {
    "health": 1.0,
    "risk": 0.0,
    "entropy": 0.0,
    "history": []
})

# =========================
# v4: PREDICTIVE FAILURE MODEL
# =========================
def predict_failure(node):
    """
    Predict future instability using trend + randomness bias
    """
    s = state[node]
    trend = sum(s["history"][-3:]) / 3 if len(s["history"]) >= 3 else 0.5

    # simulated degradation prediction
    noise = random.uniform(-0.05, 0.05)

    predicted = (1.0 - s["health"]) * 0.6 + trend * 0.3 + noise
    return max(0.0, min(1.0, predicted))


# =========================
# v5: GRAPH MUTATION ENGINE
# =========================
def mutate_graph(node, predicted_risk):
    """
    If node is unstable, rewire connections dynamically
    """
    if predicted_risk > 0.75:
        print(f"🧬 v5 MUTATION: {node} is unstable → rewiring")

        # detach from all parents
        for parent in GRAPH:
            if node in GRAPH[parent]:
                GRAPH[parent].remove(node)

        # attempt fallback reconnection
        fallback = random.choice(NODES)

        if fallback != node:
            GRAPH[fallback].append(node)
            print(f"🔁 REWIRED: {node} → {fallback}")


# =========================
# v6: ENTROPY OPTIMIZER
# =========================
def compute_entropy():
    """
    Measures system disorder (graph instability proxy)
    """
    entropy = 0.0

    for n in NODES:
        connections = len(GRAPH[n])
        entropy += abs(1 - connections * 0.25)

    return entropy / len(NODES)


def optimize_graph():
    """
    Attempts to reduce entropy by balancing connectivity
    """
    entropy = compute_entropy()

    if entropy > 0.8:
        print("⚛️ v6 OPTIMIZER: High entropy detected → stabilizing graph")

        # stabilize assistant as anchor node
        for n in NODES:
            if n != "assistant" and "assistant" not in GRAPH[n]:
                GRAPH[n].append("assistant")


# =========================
# SIMULATED HEALTH UPDATE
# =========================
def update_health(node):
    """
    Simulated runtime health decay
    """
    decay = random.uniform(-0.1, 0.05)
    state[node]["health"] = max(0.0, min(1.0, state[node]["health"] + decay))

    state[node]["history"].append(state[node]["health"])


# =========================
# CAUSAL SCORING
# =========================
def compute_risk(node, predicted):
    current = 1.0 - state[node]["health"]
    return max(current, predicted * 0.8)


# =========================
# MAIN EVOLUTION LOOP
# =========================
def run():
    print("\n🧠 OMEGA PREDICTIVE GRAPH EVOLUTION v4-v6\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        # STEP 1: UPDATE HEALTH
        for n in NODES:
            update_health(n)

        # STEP 2: PREDICT FAILURE (v4)
        predictions = {}
        for n in NODES:
            predictions[n] = predict_failure(n)

        # STEP 3: RISK COMPUTATION
        risks = {}
        for n in NODES:
            risks[n] = compute_risk(n, predictions[n])

        # STEP 4: GRAPH MUTATION (v5)
        for n in NODES:
            mutate_graph(n, risks[n])

        # STEP 5: ENTROPY OPTIMIZATION (v6)
        optimize_graph()

        # STEP 6: OUTPUT STATE
        total = 0

        for n in NODES:
            s = state[n]
            r = risks[n]
            total += r

            print("\n────────────────────────")
            print(f"NODE       : {n}")
            print(f"HEALTH     : {round(s['health'], 3)}")
            print(f"PREDICTED  : {round(predictions[n], 3)}")
            print(f"RISK       : {round(r, 3)}")
            print(f"CONNS      : {len(GRAPH[n])}")

            if r > 0.75:
                print("🚨 HIGH FUTURE FAILURE RISK")
            elif r > 0.5:
                print("⚠️ MEDIUM RISK")
            else:
                print("🟢 STABLE")

        avg = total / len(NODES)
        entropy = compute_entropy()

        print("\n════════════════════════════")
        print(f"🧠 SYSTEM RISK: {round(avg, 3)}")
        print(f"⚛️ ENTROPY: {round(entropy, 3)}")

        if avg > 0.7:
            print("🔴 SYSTEM STATE: COLLAPSE VECTOR ACTIVE")
        elif avg > 0.4:
            print("🟠 SYSTEM STATE: UNSTABLE EVOLUTION")
        else:
            print("🟢 SYSTEM STATE: STABLE EVOLUTION")

        print("════════════════════════════")

        time.sleep(10)


if __name__ == "__main__":
    run()
