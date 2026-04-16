# OMEGA KERNEL V54
# TRUE COGNITIVE EQUILIBRIUM SYSTEM

import random
import math
import time

print("[V54] TRUE COGNITIVE EQUILIBRIUM ONLINE")

# -------------------------
# SYSTEM STATE
# -------------------------
entropy = 0.3
temperature = 1.3
nodes = 10

# Targets (THIS is what creates equilibrium)
TARGET_ENTROPY = 0.6
TARGET_STABILITY = 0.75

# Memory (NEW)
stability_history = []
entropy_history = []

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

def adjust_nodes(stability):
    global nodes

    # 🔥 KEY LOGIC
    if stability < 0.65:
        nodes -= random.randint(1, 2)  # prune chaos
    elif stability > 0.80:
        nodes += random.randint(1, 2)  # expand intelligence

    nodes = max(5, min(nodes, 100))

def entropy_step():
    global entropy, temperature, nodes

    noise = random.uniform(-0.05, 0.05)

    # Node influence (more nodes = more complexity)
    node_factor = (nodes / 50)

    entropy += noise * temperature * node_factor
    entropy = clamp(entropy, 0.1, 0.9)

def detect_convergence():
    if len(stability_history) < 20:
        return False

    recent = stability_history[-20:]
    variance = max(recent) - min(recent)

    return variance < 0.05  # 🔥 convergence condition

def equilibrium_lock():
    global temperature, nodes

    # LOCK SYSTEM INTO STABLE MODE
    temperature = 0.5
    nodes = int(nodes * 0.9)

    print("[V54] 🔒 EQUILIBRIUM LOCK ENGAGED")

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

        # Save memory
        stability_history.append(stability)
        entropy_history.append(entropy)

        # 🔒 Check convergence
        if detect_convergence():
            equilibrium_lock()

        print(f"[V54] tick={tick} | entropy={entropy:.3f} | temp={temperature:.3f} | nodes={nodes} | stability={stability:.3f}")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n[V54] shutdown clean")

    print("\n[V54 SUMMARY]")
    print(f"Avg Entropy: {sum(entropy_history)/len(entropy_history):.3f}")
    print(f"Avg Stability: {sum(stability_history)/len(stability_history):.3f}")
    print(f"Final Nodes: {nodes}")
