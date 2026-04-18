import json
import time

FILE = "omega_v32_beliefs.json"

def load():
    try:
        return json.load(open(FILE))
    except:
        return {"beliefs": {}}

def reinforce(belief, strength=1.0):
    data = load()

    if belief not in data["beliefs"]:
        data["beliefs"][belief] = {"weight": 0, "history": []}

    data["beliefs"][belief]["weight"] += strength
    data["beliefs"][belief]["history"].append(time.time())

    json.dump(data, open(FILE, "w"), indent=2)

    return data["beliefs"][belief]
