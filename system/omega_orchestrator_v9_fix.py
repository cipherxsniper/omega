def run(self):
    while True:
        rec = self.recursive.step()

        agents = rec.get("agents", {})

        if not agents:
            continue

        strongest = max(agents, key=agents.get)

        print("[ORCH-v9 SAFE]", strongest, agents[strongest])
