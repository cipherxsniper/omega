# Ω CLUSTER v9.6 — CONTROL PLANE (K8s-lite)

import json
import time

from omega_node_agent_v9_6 import NodeAgent
from omega_scheduler_v9_6 import schedule
from omega_health_v9_6 import HealthEngine


class Cluster:

    def __init__(self):
        with open("omega_cluster_state_v9_6.json", "r") as f:
            self.state = json.load(f)

        self.nodes = {
            "local-node-1": NodeAgent("local-node-1")
        }

        self.boot_services()

        self.health = HealthEngine(self.state, self.nodes)

    def boot_services(self):

        for name, svc in self.state["services"].items():

            node_id = schedule(svc, self.state["nodes"])

            if not node_id:
                print("[CLUSTER] no node available for", name)
                continue

            svc["node"] = node_id

            agent = self.nodes[node_id]
            agent.start(name, svc["cmd"])

    def run(self):
        print("[Ω CLUSTER v9.6 ONLINE — K8s-lite CONTROL PLANE]")

        self.health.reconcile()


if __name__ == "__main__":
    Cluster().run()
