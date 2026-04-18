import os
import time
import random
import json
import math
import hashlib
from collections import deque, defaultdict

print("🧠 WINK_WINK v18 CAUSAL EVOLUTION ENGINE ONLINE")

# =========================
# MEMORY (PERSISTENT)
# =========================
MEM_PATH = "logs/wink_v18_memory.json"
os.makedirs("logs", exist_ok=True)

def load_memory():
    if os.path.exists(MEM_PATH):
        try:
            return json.load(open(MEM_PATH))
        except:
            pass
    return {"states": [], "sent": []}

def save_memory(m):
    json.dump(m, open(MEM_PATH,"w"))

memory = load_memory()

# =========================
# SWARM NODES
# =========================
NODES = 250
nodes = [{"state": random.random(), "bias": random.uniform(0.3,0.9)} for _ in range(NODES)]

# =========================
# FILE DRIFT SCAN (WITH EVOLUTION)
# =========================
def scan():
    g = defaultdict(float)

    for root,_,files in os.walk("."):
        for f in files:
            if f.endswith(".py"):
                try:
                    txt = open(os.path.join(root,f),"r",errors="ignore").read(2000)

                    base = {
                        "brain": txt.count("brain"),
                        "memory": txt.count("memory"),
                        "node": txt.count("node"),
                        "swarm": txt.count("swarm"),
                        "kernel": txt.count("kernel")
                    }

                    # 🔥 entropy injection (CRITICAL FIX)
                    noise = random.uniform(0.85, 1.15)

                    for k,v in base.items():
                        g[k] += v * noise

                except:
                    pass

    return dict(g)

# =========================
# NODE DYNAMICS (REAL EVOLUTION)
# =========================
def step_nodes():
    total = 0

    for n in nodes:
        drift = random.uniform(-0.05,0.05)

        # coupling effect (nodes influence each other)
        n["state"] += drift * n["bias"]
        n["state"] *= (0.98 + random.random()*0.04)

        n["state"] = max(0,min(1,n["state"]))
        total += n["state"]

    return total / NODES

# =========================
# CAUSAL STATE VECTOR (NEW CORE)
# =========================
def build_state(graph, signal, prev):
    dominant = max(graph, key=graph.get) if graph else "unknown"

    entropy = random.random() * abs(signal - (prev["signal"] if prev else 0.5))

    novelty = random.random()

    return {
        "signal": signal,
        "dominant": dominant,
        "entropy": entropy,
        "novelty": novelty,
        "node_avg": signal
    }

# =========================
# STATE MEMORY MATCHING
# =========================
def distance(a,b):
    return abs(a["signal"]-b["signal"]) + abs(a["entropy"]-b["entropy"])

def match(state):
    best = None
    best_d = 999

    for m in memory["states"]:
        d = distance(state,m)
        if d < best_d:
            best_d = d
            best = m

    return best, best_d

# =========================
# REAL SENTENCE GENERATOR (STATE-DRIVEN)
# =========================
def think(state, match, dist):

    dom = state["dominant"]

    pressure = "high drift" if state["entropy"] > 0.4 else "stable transition"

    if match:
        memory_note = f"pattern recurrence detected at distance {round(dist,3)}"
    else:
        memory_note = "no prior structural alignment detected"

    sentence = (
        f"Omega is processing {dom} under {pressure}, "
        f"signal={round(state['signal'],3)}, "
        f"{memory_note}, "
        f"novelty={round(state['novelty'],3)}"
    )

    return sentence

# =========================
# MAIN LOOP
# =========================
tick = 0
prev = None

while True:

    graph = scan()
    signal = step_nodes()

    state = build_state(graph, signal, prev)

    match_state, dist = match(state)

    thought = think(state, match_state, dist)

    memory["states"].append(state)
    memory["states"] = memory["states"][-200:]

    save_memory(memory)

    print(f"\n🧠 TICK {tick}")
    print(f"STATE: signal={round(state['signal'],3)} entropy={round(state['entropy'],3)} novelty={round(state['novelty'],3)}")
    print(f"DOMINANT={state['dominant']} | DISTANCE={round(dist,3)}")
    print(f"THOUGHT: {thought}")

    prev = state
    tick += 1
    time.sleep(1)
