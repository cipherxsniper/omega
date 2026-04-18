import sys
import time

print("🧠 OBSERVER PATCH ACTIVE - FORCED LOG MODE", flush=True)

sys.stdout = open("logs/observer.log", "a", buffering=1)

print("🧠 LOG PIPE ACTIVE", flush=True)

while True:
    print("heartbeat: observer alive", flush=True)
    time.sleep(2)
