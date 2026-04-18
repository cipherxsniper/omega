import json
import time

FILE = "omega_v32_identity.json"

def load():
    try:
        return json.load(open(FILE))
    except:
        return {
            "identity": {
                "self_label": "omega",
                "stability": 0.5,
                "traits": []
            }
        }

def update_trait(trait, weight=0.1):
    data = load()

    data["identity"]["traits"].append({
        "trait": trait,
        "weight": weight,
        "time": time.time()
    })

    json.dump(data, open(FILE, "w"), indent=2)

    return data
