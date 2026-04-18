import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# -------------------------
# NODE REGISTRY
# -------------------------

def nodes():
    return list(r.smembers("omega.nodes.active"))


def weight(node):
    return float(r.get(f"omega.nodes.weight.{node}") or 1.0)


# -------------------------
# VOTING
# -------------------------

def vote(tick, node, value):
    r.set(f"omega.nodes.vote.{tick}.{node}", value, ex=10)


def get_votes(tick):
    data = []
    for n in nodes():
        v = r.get(f"omega.nodes.vote.{tick}.{n}")
        if v is not None:
            data.append((n, float(v)))
    return data


# -------------------------
# CONSENSUS ENGINE
# -------------------------

def compute(tick):
    votes = get_votes(tick)

    if not votes:
        return 0.0, 0.0

    total_w = 0
    total = 0

    for n, v in votes:
        w = weight(n)
        total += v * w
        total_w += w

    consensus = total / total_w if total_w else 0

    # stability = agreement level
    variance = sum((v - consensus) ** 2 for _, v in votes) / len(votes)
    stability = max(0.0, 1.0 - variance)

    r.set("omega.consensus.last", consensus)
    r.set("omega.consensus.score", stability)

    return consensus, stability
