from omega_execution_v74 import OmegaExecutionV74

g = OmegaExecutionV74()

g.register_node("temporal", lambda m,p: {"health": 0.6})
g.register_node("diagnostic", lambda m,p: {"health": 0.8})
g.register_node("repair", lambda m,p: {"health": 0.9})

g.connect("temporal", "diagnostic", 0.7)
g.connect("diagnostic", "repair", 0.8)

for tick in range(5):
    result = g.route("temporal", {"drift": 40}, steps=5)

    print("\n[TICK]", tick)
    print("FINAL:", result["final_node"])
    print("SCORES:", result["node_scores"])
