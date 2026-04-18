import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

TARGET = 24

def run():
    nodes = len(r.smembers("omega.nodes.active"))

    if nodes < TARGET:
        print(f"⚠️ REAL deficit: {nodes}/{TARGET}")
    else:
        print(f"✅ Mesh stable: {nodes}/{TARGET}")


if __name__ == "__main__":
    while True:
        run()
        import time
        time.sleep(2)
