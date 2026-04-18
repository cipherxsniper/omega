import redis
import time

def wait():
    for i in range(30):
        try:
            r = redis.Redis(host="127.0.0.1", port=6379)
            if r.ping():
                print("🟢 REDIS CONFIRMED READY (PONG)")
                return True
        except:
            pass

        print(f"⏳ waiting for redis... ({i+1})")
        time.sleep(1)

    raise Exception("REDIS FAILED TO START")

if __name__ == "__main__":
    wait()
