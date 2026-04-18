from core.redis_safe import get_redis
import json
import time
import statistics

r = get_redis()

node_scores = {}

def score(payload):
    cpu = payload.get("cpu", 0)
    mem = payload.get("memory", 0)
    load = payload.get("load", 0)
    return (1 - abs(cpu - 0.5)) + (1 - abs(mem - 0.5)) + (1 - abs(load - 0.5))

def handle(event):
    node = event["node"]
    payload = event["payload"]

    s = score(payload)

    node_scores.setdefault(node, [])
    node_scores[node].append(s)

    avg_score = statistics.mean(node_scores[node][-20:])

    # detect anomaly
    anomaly = s < 0.5

    # dominant brain
    dominant = max(node_scores.items(), key=lambda x: statistics.mean(x[1][-20:]))[0]

    print("\n🧠 OMEGA v20 OBSERVER")
    print(f"Node: {node}")
    print(f"Score: {s:.3f} | Avg: {avg_score:.3f}")
    print(f"Anomaly: {anomaly}")
    print(f"👑 Dominant Brain: {dominant}")

    if node == dominant:
        print("⚡ ACTIVE COORDINATOR NODE")

    # publish swarm state
    r.publish("omega.swarm.state", json.dumps({
        "node": node,
        "score": s,
        "dominant": dominant,
        "anomaly": anomaly
    }))
