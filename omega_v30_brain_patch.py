import redis
import time

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

ALPHA = 0.2
prev_avg = None

def smooth(avg):
    global prev_avg
    if prev_avg is None:
        prev_avg = avg
        return avg

    avg = ALPHA * avg + (1 - ALPHA) * prev_avg
    prev_avg = avg
    return avg


def get_node_count():
    try:
        return len(r.smembers("omega.nodes.active"))
    except:
        return 0


def acquire_leader(node_id):
    return r.set("omega.brain.leader", node_id, nx=True, ex=3)


def is_leader(node_id):
    leader = r.get("omega.brain.leader")

    if leader == node_id:
        r.expire("omega.brain.leader", 3)
        return True

    if leader is None:
        return acquire_leader(node_id)

    return False


def brain_tick(signals, tick):
    raw_avg = sum(signals) / len(signals) if signals else 0
    avg = smooth(raw_avg)

    r.set("omega.cognition.avg", avg)

    print(f"🌐 SWARM COGNITION AVG = {avg:.3f}")
    print(f"📊 Active nodes: {get_node_count()} | tick={tick}")
