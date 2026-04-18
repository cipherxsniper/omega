import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

print("🧠 CORE LOADED SAFE")

def nodes():
    try:
        return list(r.smembers("omega.nodes.active"))
    except:
        return []

def weight(n):
    try:
        return float(r.get(f"omega.nodes.weight.{n}") or 1.0)
    except:
        return 1.0

def set_weight(n, w):
    try:
        r.set(f"omega.nodes.weight.{n}", float(w))
    except:
        pass
