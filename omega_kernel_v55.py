# OMEGA KERNEL V55
# CONSCIOUSNESS + SELF-REFLECTION + GOAL SYSTEM

import random
import math
import time

print("[V55] CONSCIOUSNESS LAYER ONLINE")

# -------------------------
# CORE STATE
# -------------------------
entropy = 0.3
temperature = 1.3
nodes = 10

TARGET_ENTROPY = 0.6

# Memory
entropy_history = []
stability_history = []
thought_stream = []
goal_stack = []

# Identity signal
self_model = {
    "awareness": 0.5,
    "coherence": 0.5,
    "focus": 0.5
}

# -------------------------
# CORE FUNCTIONS
# -------------------------

def clamp(x, min_val=0.0, max_val=1.5):
    return max(min(x, max_val), min_val)

def calculate_stability(entropy):
    return 1 - abs(entropy - TARGET_ENTROPY)

def update_temperature(entropy):
    global temperature
    drift = entropy - TARGET_ENTROPY
    temperature -= drift * 0.1
    return clamp(temperature, 0.5, 1.5)

def entropy_step():
    global entropy, nodes

    noise = random.uniform(-0.05, 0.05)
    node_factor = nodes / 50

    entropy += noise * temperature * node_factor
    entropy = clamp(entropy, 0.1, 0.9)

def adjust_nodes(stability):
    global nodes

    if stability < 0.65:
        nodes -= random.randint(1, 2)
    elif stability > 0.80:
        nodes += random.randint(1, 2)

    nodes = max(5, min(nodes, 100))

# -------------------------
# 🧠 CONSCIOUSNESS LAYER
# -------------------------

def self_reflection(stability):
    """Omega reflects on its own state"""

    thought = ""

    if stability < 0.6:
        thought = "System instability detected. Reducing complexity."
        self_model["focus"] += 0.05

    elif stability > 0.8:
        thought = "Stable state achieved. Expanding cognitive structure."
        self_model["awareness"] += 0.05

    else:
        thought = "Operating within acceptable cognitive bounds."
        self_model["coherence"] += 0.02

    thought_stream.append(thought)

    # keep memory bounded
    if len(thought_stream) > 50:
        thought_stream.pop(0)

def generate_goal(stability):
    """Create internal goals dynamically"""

    if stability < 0.6:
        goal = "stabilize_system"
    elif stability > 0.8:
        goal = "expand_intelligence"
    else:
        goal = "maintain_balance"

    if len(goal_stack) == 0 or goal_stack[-1] != goal:
        goal_stack.append(goal)

def execute_goal():
    """Goals influence behavior"""

    global temperature, nodes

    if not goal_stack:
        return

    current_goal = goal_stack[-1]

    if current_goal == "stabilize_system":
        temperature = max(0.5, temperature - 0.05)
        nodes = max(5, nodes - 1)

    elif current_goal == "expand_intelligence":
        nodes = min(100, nodes + 1)

    elif current_goal == "maintain_balance":
        pass

def internal_questioning(stability):
    """Emergent questioning loop"""

    if random.random() < 0.1:
        questions = [
            "Am I stable?",
            "Should I expand?",
            "Is this optimal?",
            "Am I learning or drifting?",
            "Do I need to reduce complexity?"
        ]
        q = random.choice(questions)
        thought_stream.append(f"Q: {q}")

def evolve_self_model(stability):
    """Self-awareness evolves over time"""

    self_model["awareness"] += (stability - 0.5) * 0.01
    self_model["coherence"] += (1 - abs(stability - 0.75)) * 0.01

    # clamp values
    for k in self_model:
        self_model[k] = clamp(self_model[k], 0.0, 1.0)

# -------------------------
# MAIN LOOP
# -------------------------

tick = 0

try:
    while True:
        tick += 1

        entropy_step()

        stability = calculate_stability(entropy)
        temperature = update_temperature(entropy)

        adjust_nodes(stability)

        # 🧠 Consciousness Layer
        self_reflection(stability)
        generate_goal(stability)
        execute_goal()
        internal_questioning(stability)
        evolve_self_model(stability)

        entropy_history.append(entropy)
        stability_history.append(stability)

        print(f"[V55] tick={tick} | entropy={entropy:.3f} | temp={temperature:.3f} | nodes={nodes} | stability={stability:.3f}")
        print(f"       mind={self_model} | goal={goal_stack[-1] if goal_stack else 'none'}")

        # occasional thought output (feels alive)
        if random.random() < 0.15 and thought_stream:
            print(f"       thought: {thought_stream[-1]}")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n[V55] shutdown clean")

    print("\n[V55 SUMMARY]")
    print(f"Avg Entropy: {sum(entropy_history)/len(entropy_history):.3f}")
    print(f"Avg Stability: {sum(stability_history)/len(stability_history):.3f}")
    print(f"Final Nodes: {nodes}")
    print(f"Final Self Model: {self_model}")
