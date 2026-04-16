import time
import random
from collections import defaultdict, deque

# =====================================================
# 🧠 CAUSAL GRAPH (STRUCTURE LAYER)
# =====================================================
GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

NODES = list(GRAPH.keys())

# =====================================================
# 🧬 IDENTITY CORE (v8 SELF-AWARE MODEL)
# =====================================================
identity = defaultdict(lambda: {
    "role": "UNKNOWN",
    "behavior_signature": deque(maxlen=50),
    "causal_profile": {
        "failure_triggers": defaultdict(int),
        "stability_triggers": defaultdict(int)
    },
    "self_model": "undefined",
    "confidence": 0.0
})

# =====================================================
# 🧠 SIMULATED RUNTIME SIGNAL (replace with real logs later)
# =====================================================
def runtime_signal(node):
    return random.choice([
        "STABLE",
        "STABLE",
        "DEGRADED",
        "FAILURE"
    ])

# =====================================================
# 🧬 ROLE CLASSIFIER (v8 CORE)
# =====================================================
def classify_role(node):
    if "bus" in node:
        return "SERVICE"
    if "assistant" in node:
        return "SERVICE"
    if "emitter" in node:
        return "TASK"
    if "memory" in node:
        return "HYBRID"
    return "UNKNOWN"

# =====================================================
# 🧠 UPDATE BEHAVIOR SIGNATURE
# =====================================================
def update_behavior(node, event):
    identity[node]["behavior_signature"].append(event)

# =====================================================
# 🧠 CAUSAL LEARNING ENGINE
# =====================================================
def update_causal_profile(node):
    sig = list(identity[node]["behavior_signature"])

    for i in range(len(sig) - 1):
        cause = sig[i]
        result = sig[i + 1]

        if result == "FAILURE":
            identity[node]["causal_profile"]["failure_triggers"][cause] += 1

        if result == "STABLE":
            identity[node]["causal_profile"]["stability_triggers"][cause] += 1

# =====================================================
# 🧠 SELF-MODEL GENERATION (NEW CORE FEATURE)
# =====================================================
def build_self_model(node):
    profile = identity[node]["causal_profile"]

    fail = sum(profile["failure_triggers"].values())
    stable = sum(profile["stability_triggers"].values())

    role = identity[node]["role"]

    if fail > stable:
        model = f"{node} behaves as unstable {role} with collapse-prone transitions"
        confidence = 0.7
    elif stable > fail:
        model = f"{node} behaves as stable {role} with predictable execution pattern"
        confidence = 0.8
    else:
        model = f"{node} behavior unclear; insufficient causal definition"
        confidence = 0.4

    identity[node]["self_model"] = model
    identity[node]["confidence"] = confidence

# =====================================================
# 🧠 SYSTEM EVOLUTION LOOP
# =====================================================
def run():
    print("\n🧠 OMEGA SELF-AWARE CAUSAL IDENTITY v8\n")

    # init roles
    for node in NODES:
        identity[node]["role"] = classify_role(node)

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        for node in NODES:
            event = runtime_signal(node)

            update_behavior(node, event)
            update_causal_profile(node)
            build_self_model(node)

            print("\n────────────────────────")
            print("NODE     :", node)
            print("ROLE     :", identity[node]["role"])
            print("EVENT    :", event)
            print("MODEL    :", identity[node]["self_model"])
            print("CONF     :", round(identity[node]["confidence"], 3))

            if event == "FAILURE":
                print("🚨 CAUSAL EVENT: FAILURE OBSERVED")
            elif event == "DEGRADED":
                print("⚠️ CAUSAL EVENT: INSTABILITY")
            else:
                print("🟢 CAUSAL EVENT: STABLE")

        print("\n════════════════════════════")
        print("🧠 SELF-MODEL EVOLUTION ACTIVE")
        print("════════════════════════════")

        time.sleep(4)


if __name__ == "__main__":
    run()
