# Ω HEALTH ENGINE v9.6 — RECONCILER LOOP

import time

class HealthEngine:
    def __init__(self, cluster_state, node_agents):
        self.state = cluster_state
        self.nodes = node_agents

    def reconcile(self):
        while True:

            for service_name, svc in self.state["services"].items():
                node_id = svc["node"]
                agent = self.nodes[node_id]

                alive = agent.is_alive(service_name)

                if not alive:
                    print(f"[HEALTH] FAILED: {service_name}")
                    if svc.get("critical", False):
                        print(f"[HEALTH] RESTARTING CRITICAL: {service_name}")
                        agent.restart(service_name)

            time.sleep(1)
