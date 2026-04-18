import difflib

def detect_conflict(belief_a, belief_b):
    similarity = difflib.SequenceMatcher(None, belief_a, belief_b).ratio()

    if similarity < 0.2:
        return {
            "conflict": True,
            "reason": "low semantic similarity"
        }

    return {
        "conflict": False,
        "reason": "aligned or compatible"
    }

def resolve(conflicts):
    if not conflicts:
        return "stable"

    return "requires_reweighting"
