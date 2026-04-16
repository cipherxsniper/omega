from pathlib import Path

ROOT = Path.home() / "Omega"

EXEC_TYPE = {
    "swarm_bus": "SERVICE",
    "memory": "TASK",
    "assistant": "SERVICE",
    "emitter": "TASK"
}


def mock_inputs():
    return {
        "swarm_bus": {"risk": 0.8, "collapse": 0.7},
        "memory": {"risk": 0.6, "collapse": 0.5},
        "assistant": {"risk": 0.2, "collapse": 0.1},
        "emitter": {"risk": 0.3, "collapse": 0.2}
    }


def decide(module, data):
    score = (data["risk"] * 0.6) + (data["collapse"] * 0.4)
    t = EXEC_TYPE[module]

    if score > 0.75:
        return "RESTART_SERVICE" if t == "SERVICE" else "RETRY_TASK"

    if score > 0.5:
        return "SOFT_RESTART" if t == "SERVICE" else "DEFER_TASK"

    if score > 0.3:
        return "MONITOR"

    return "NO_ACTION"


def run():
    data = mock_inputs()

    print("\n🧠 OMEGA SELF-HEALING POLICY ENGINE V1\n")

    for m, v in data.items():
        action = decide(m, v)
        print(f"{m} → {action}")


if __name__ == "__main__":
    run()
