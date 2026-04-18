# 🧠 Omega v17 Runtime Engine

from omega_v17.memory.global_state_v17 import GlobalState
from omega_v17.mesh.communication_mesh import CommunicationMesh
from omega_v17.leaders.leadership_engine import LeadershipEngine
from omega_v17.clusters.cluster_engine import ClusterEngine
from omega_v17.evolution.evolution_engine import EvolutionEngine

import time

state = GlobalState()
mesh = CommunicationMesh(state)
leader = LeadershipEngine()
cluster = ClusterEngine()
evolution = EvolutionEngine()

nodes = ["attention", "goal", "memory", "stability"]

while True:

    for n in nodes:

        node = state.get_node(n)

        # communication
        for m in nodes:
            if n != m:
                mesh.send_signal(n, m)

        # clustering
        cluster.assign_cluster(state, n)

        # evolution
        evolution.evolve_node(node)

        # leadership decay check
        leader.decay(node)

    state.update()

    print("🧠 Omega v17 cycle complete")
    time.sleep(1)
