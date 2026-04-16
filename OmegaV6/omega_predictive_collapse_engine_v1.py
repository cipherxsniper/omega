import subprocess
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"

GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

history = defaultdict(lambda: deque(maxlen=5))


def ps_snapshot():
    try:
        out = subprocess.check_output(["ps", "-A"], text=True)
        return out.lower().splitlines()
    except Exception:
        return []


def is_running(ps_lines, signature):
    return any(signature in line for line in ps_lines)


def semantic_health(module):
    path = LOGS / f"{module}.log"
    if not path.exists():
        return 0.3

    data = path.read_text(errors="ignore").lower()

    score = 0.5
    if "heartbeat" in data or "alive" in data:
        score += 0.3
    if "error" in data or "traceback" in data:
        score -= 0.4
    if len(data.strip()) == 0:
        score -= 0.2

    return max(0.0, min(1.0, score))


def runtime_health(module, ps_lines):
    return 1.0 if is_running(ps_lines, module) else 0.2


def combined_health(module, ps_lines):
    return (semantic_health(module) * 0.6) + (runtime_health(module, ps_lines) * 0.4)


def update_history(module, value):
    history[module].append(value)


def trend(values):
    if len(values) < 3:
        return "UNKNOWN"
    if values[-1] < values[-2] < values[-3]:
        return "DECLINING"
    if values[-1] > values[-2] > values[-3]:
        return "IMPROVING"
    return "STABLE"


def collapse_risk(module, base_health):
    update_history(module, base_health)

    r = 1.0 - base_health
    t = trend(history[module])

    if t == "DECLINING":
        r += 0.25
    elif t == "IMPROVING":
        r -= 0.15
    else:
        r += 0.1

    return max(0.0, min(1.0, r))


def downstream_pressure(module, risks):
    pressure = 0.0
    for parent, children in GRAPH.items():
        if module in children:
            pressure += risks.get(parent, 0) * 0.4
    return pressure


def run():
    ps = ps_snapshot()

    modules = list(GRAPH.keys())
    health, risk, pressure = {}, {}, {}

    print("\n🧠 OMEGA PREDICTIVE COLLAPSE ENGINE V1\n")

    for m in modules:
        health[m] = combined_health(m, ps)

    for m in modules:
        risk[m] = collapse_risk(m, health[m])

    for m in modules:
        pressure[m] = downstream_pressure(m, risk)

    for m in modules:
        final = min(1.0, risk[m] + pressure[m])

        print("──────────────────────────────")
        print("MODULE:", m)
        print("HEALTH:", round(health[m], 3))
        print("RISK:", round(risk[m], 3))
        print("PRESS:", round(pressure[m], 3))
        print("FINAL:", round(final, 3))

        if final > 0.75:
            print("🚨 HIGH COLLAPSE RISK")
        elif final > 0.5:
            print("⚠️ MEDIUM RISK")
        else:
            print("🟢 LOW RISK")

    avg = sum(risk.values()) / len(risk)

    print("\nSYSTEM INDEX:", round(avg, 3))


if __name__ == "__main__":
    run()
