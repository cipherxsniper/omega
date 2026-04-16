import time
from omega_execution_graph_v69 import OmegaExecutionGraphV69

g = OmegaExecutionGraphV69()

g.add_node("temporal", lambda m,p: {"health": 1.0 - (p["drift"]*0.01), "output":"temporal", "signals":p})
g.add_node("diagnostic", lambda m,p: {"health":0.8,"output":"diagnostic","signals":{}})
g.set_repair_node(lambda m,p: {"health":0.9,"output":"repair","signals":{"fixed":True}})

g.connect("temporal","diagnostic")

tick = 0

while tick < 1000:
    result = g.route(
        "temporal",
        {},
        {"score": 0.7, "drift": 40},
        tick_id=tick
    )

    print(result)

    tick += 1
    time.sleep(1)
