from omega_core.omega_router_v10_5 import Router
import time

r=Router()
nodes=["memory","goal","attention","stability"]

print("🧠 OMEGA v10.5 RUNNING")

while True:
    print(r.tick(nodes))
    time.sleep(2)
