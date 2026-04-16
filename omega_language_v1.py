import os
import random
import time

# =========================
# 🧠 OMEGA LANGUAGE v1
# =========================

BELIEF_GRAPH = {
    "coherence": 0.5,
    "entropy": 0.5,
    "stability": 0.5,
    "intent": 0.5
}


# =========================
# ⚡ CORE OPERATIONS
# =========================

def think(args):
    # simulate internal reasoning shift
    delta = random.uniform(-0.05, 0.05)
    BELIEF_GRAPH["coherence"] = max(0, min(1, BELIEF_GRAPH["coherence"] + delta))
    print(f"[Ω-THINK] coherence={BELIEF_GRAPH['coherence']:.3f}")


def mutate(args):
    key = random.choice(list(BELIEF_GRAPH.keys()))
    delta = random.uniform(-0.1, 0.1)
    BELIEF_GRAPH[key] = max(0, min(1, BELIEF_GRAPH[key] + delta))
    print(f"[Ω-MUTATE] {key} -> {BELIEF_GRAPH[key]:.3f}")


def observe(args):
    print("[Ω-OBSERVE]")
    for k, v in BELIEF_GRAPH.items():
        print(f"  {k}: {v:.3f}")


def set_value(args):
    # SET key value
    if len(args) < 2:
        print("SET <key> <value>")
        return
    k = args[0]
    v = float(args[1])
    BELIEF_GRAPH[k] = max(0, min(1, v))
    print(f"[Ω-SET] {k} = {v}")


def run_system(cmd):
    os.system(cmd)


# =========================
# 🧠 PARSER
# =========================

def execute_line(line):
    parts = line.strip().split()
    if not parts:
        return

    cmd = parts[0].upper()
    args = parts[1:]

    if cmd == "THINK":
        think(args)

    elif cmd == "MUTATE":
        mutate(args)

    elif cmd == "OBSERVE":
        observe(args)

    elif cmd == "SET":
        set_value(args)

    elif cmd == "RUN":
        run_system(" ".join(args))

    elif cmd == "WAIT":
        time.sleep(float(args[0]) if args else 1)

    else:
        print(f"[Ω-LANG] Unknown command: {cmd}")


# =========================
# 🚀 FILE EXECUTOR
# =========================

def run_file(file):
    print(f"[Ω-LANG] executing: {file}")

    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                execute_line(line)


# =========================
# 🧠 CLI MODE
# =========================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python omega_language_v1.py script.omega")
        exit()

    run_file(sys.argv[1])
