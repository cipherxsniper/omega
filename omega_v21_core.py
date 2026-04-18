import random
import time

# =========================
# NODE MODEL
# =========================

class QuantumNode:
    def __init__(self, name):
        self.name = name
        self.memory_weight = random.uniform(0.3, 0.7)
        self.stability = random.uniform(0.4, 0.9)

    def evaluate(self, packet):
        return (
            self.memory_weight * 0.6 +
            self.stability * 0.4 +
            random.uniform(-0.05, 0.05)
        )

# =========================
# GLOBAL COGNITIVE FIELD
# =========================

omega_field = {
    "packets": [],
    "transitions": [],
    "attractor_map": {}
}

# =========================
# STATE PACKET
# =========================

def create_packet(signal, source):
    return {
        "id": f"pkt_{random.randint(1000,9999)}",
        "signal": signal,
        "source": source,
        "amplitude_vector": {},
        "phase_noise": 0.05,
        "history_trace": []
    }

# =========================
# SUPERPOSITION PROPAGATION
# =========================

def propagate(packet, nodes):
    candidates = {}

    for node in nodes:
        weight = packet["amplitude_vector"].get(node.name, 0)
        noise = random.uniform(-packet["phase_noise"], packet["phase_noise"])
        candidates[node.name] = max(0.0, weight + noise)

    return candidates

# =========================
# COLLAPSE FUNCTION
# =========================

def collapse(candidates):
    total = sum(candidates.values())
    r = random.uniform(0, total)

    acc = 0
    for node, w in candidates.items():
        acc += w
        if acc >= r:
            return node

# =========================
# MEMORY FIELD INFLUENCE
# =========================

def observe(node, packet):
    bias = node.memory_weight
    packet["amplitude_vector"][node.name] = bias

# =========================
# TRACE SYSTEM
# =========================

def log_transition(packet, frm, to):
    packet["history_trace"].append({
        "from": frm,
        "to": to,
        "time": time.time()
    })

    key = f"{frm}->{to}"
    omega_field["attractor_map"][key] = omega_field["attractor_map"].get(key, 0) + 1

# =========================
# RUN CYCLE
# =========================

def run_cycle(nodes):
    packet = create_packet("signal", nodes[0].name)

    for node in nodes:
        observe(node, packet)

    candidates = propagate(packet, nodes)
    chosen = collapse(candidates)

    log_transition(packet, packet["source"], chosen)

    return packet, chosen
