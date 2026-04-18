from omega_core.omega_router_v10_6 import Router
import time

r = Router()

print("🧠 OMEGA v10.6 EVOLUTION LOOP ONLINE")

while True:
    state = r.tick()
    print(state)
    time.sleep(5)   # IMPORTANT: prevents runaway CPU usage
