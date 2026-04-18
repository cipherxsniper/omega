import time
import random

from omega_cluster_brain_v15 import ClusterBrain
from omega_swarm_policy_v15 import SwarmPolicy
from omega_moe_router_v15 import MoERouter
from omega_evolution_engine_v15 import EvolutionEngine


brains = [
    ClusterBrain("attention"),
    ClusterBrain("goal"),
    ClusterBrain("memory"),
    ClusterBrain("stability")
]

for i in range(len(brains)):
    for j in range(len(brains)):
        if i != j:
            brains[i].connect(brains[j])

swarm = SwarmPolicy()
router = MoERouter()
evolver = EvolutionEngine()


while True:

    global_signal = random.uniform(0.1, 0.9)

    outputs = swarm.propagate(brains, global_signal)

    winner, scores = router.route(outputs)

    print("\n🧠 CLUSTER BRAIN STATE")
    print("WINNER:", winner)

    for k, v in scores.items():
        print(k, "=>", round(v, 3))

    # feedback loop (learning signal)
    for b in brains:
        feedback = scores[b.name] - 0.5
        b.update(feedback)
        evolver.mutate(b)

    # selection pressure (neuroevolution step)
    brains = evolver.selection_pressure(brains)

    time.sleep(1)
