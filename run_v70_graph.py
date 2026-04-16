import time
from omega_execution_graph_v70 import OmegaExecutionGraphV70

g = OmegaExecutionGraphV70()

g.add_node("temporal", lambda m,p: {
    "health": 1.0 - (p["drift"] * 0.01),
    "output": "temporal",
    "signals": p
})

g.add_node("diagnostic", lambda m,p: {
    "health": 0.8,
    "output": "diagnostic",
    "signals": {}
})

g.add_node("stability", lambda m,p: {
    "health": 0.9,
    "output": "stability",
    "signals": {}
})

g.set_repair_node(lambda m,p: {
    "health": 0.95,
    "output": "repair",
    "signals": {"fixed": True}
})

g.connect("temporal", "diagnostic", weight=0.8)
g.connect("diagnostic", "stability", weight=0.6)

tick = 0

while tick < 10:
    result = g.route(
        "temporal",
        {},
        {"score": 0.7, "drift": 40},
        tick_id=tick
    )

    print("\n[TICK]", tick)
    print("FINAL HEALTH:", result["final_health"])
    print("MEMORY:", result["node_memory"])

    tick += 1
    time.sleep(1)
