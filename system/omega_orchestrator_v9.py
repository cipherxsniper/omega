class OmegaOrchestratorV9:

    def run(self):
        while True:
            try:
                rec = self.recursive.step()

                # 🔒 SAFETY: normalize structure
                if not isinstance(rec, dict):
                    rec = {"agents": {}, "status": "invalid"}

                agents = rec.get("agents", {
                    "brain_0": 0.0,
                    "brain_1": 0.0,
                    "brain_2": 0.0,
                    "brain_3": 0.0
                })

                # prevent KeyError crash
                if not isinstance(agents, dict) or len(agents) == 0:
                    agents = {
                        "brain_0": 0.0,
                        "brain_1": 0.0,
                        "brain_2": 0.0,
                        "brain_3": 0.0
                    }

                strongest = max(agents, key=agents.get)

                rec["agents"] = agents
                rec["strongest"] = strongest

                print("[ORCH-v9] swarm:", {
                    "status": "active",
                    "strongest": strongest,
                    "score": agents[strongest]
                })

            except Exception as e:
                print("[ORCH-v9 SAFE RECOVERY]", str(e))
                continue
