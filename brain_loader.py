import os, json

BRAIN_DIR = os.path.expanduser("~/Omega/brains")

def load_brains():
    rules = {
        "box1": {"friction": 0.98, "bounce": 1.0},
        "box2": {"collapseRate": 0.03, "rejectRate": 0.02},
        "box3": {"cloneRate": 0.02, "mutation": 0.01}
    }

    try:
        for f in os.listdir(BRAIN_DIR):
            if not f.endswith(".json"):
                continue

            with open(os.path.join(BRAIN_DIR, f)) as file:
                data = json.load(file)

                for box in rules:
                    for k in rules[box]:
                        if box in data and k in data[box]:
                            rules[box][k] += data[box][k]

        return rules

    except:
        return rules
