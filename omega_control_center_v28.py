import redis
import time
import subprocess
import uuid
import os

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

STREAM = "omega.telemetry"

NODES = {}
MAX_NODES = 5

def log(tag, node, msg):
    line = f"[{tag}] [{node}] {msg}"
    print(line)
    r.xadd(STREAM, {"log": line})

def spawn_node():
    node_id = f"node_{uuid.uuid4().hex[:6]}"
    env = os.environ.copy()
    env["NODE_ID"] = node_id

    p = subprocess.Popen(["python3", "omega_node_v28.py"], env=env)
    NODES[node_id] = p

    r.sadd("omega.nodes", node_id)
    log("HEAL", node_id, "spawned")

def check_health():
    alive = r.scard("omega.nodes")
    log("STATE", "SYSTEM", f"nodes={alive}")

    if alive < MAX_NODES:
        spawn_node()

def read_signals():
    signals = []
    for n in r.smembers("omega.nodes"):
        v = r.get(f"omega.signal.{n}")
        if v:
            signals.append(float(v))

    if signals:
        avg = sum(signals)/len(signals)
        log("BRAIN", "SYSTEM", f"avg_signal={avg:.3f}")

def monitor_redis():
    try:
        r.ping()
    except:
        log("ERROR", "REDIS", "reconnecting...")

while True:
    monitor_redis()
    check_health()
    read_signals()
    time.sleep(2)
