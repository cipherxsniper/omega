import json
import time

GOV_FILE = "omega_v31_governance.json"

DEFAULT_STATE = {
    "policies": {
        "allow_self_modify": True,
        "min_votes_required": 2,
        "reject_if_conflict": True
    },
    "agents": ["reasoner", "critic", "optimizer"],
    "history": []
}

def load():
    try:
        return json.load(open(GOV_FILE))
    except:
        return DEFAULT_STATE

def save(state):
    json.dump(state, open(GOV_FILE, "w"), indent=2)
