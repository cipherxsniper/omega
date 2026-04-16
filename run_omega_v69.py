from omega_execution_graph_v69 import OmegaExecutionGraphV69


def temporal(m,p):
    return {'health': 1.0 - (p['drift']*0.01), 'output':'temporal processed', 'signals':p}

def diagnostic(m,p):
    return {'health':0.8,'output':'diagnostic ok','signals':{'check':True}}

def repair(m,p):
    return {'health':0.9,'output':'repair applied','signals':{'fixed':True}}


graph = OmegaExecutionGraphV69()

graph.add_node("temporal", temporal)
graph.add_node("diagnostic", diagnostic)
graph.set_repair_node(repair)

graph.connect("temporal", "diagnostic")

result = graph.route(
    "temporal",
    memory={},
    payload={"score": 0.7, "drift": 40}
)

print("\n[Ω v6.9 RESULT]")
print(result)
