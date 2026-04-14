from system.omega_governance_v6 import OmegaGovernanceV6

class GovernedOrchestrator:
    def __init__(self, recursive_engine):
        self.recursive = recursive_engine
        self.governor = OmegaGovernanceV6()

        # 🧠 enforce interface safety
        self.recursive = self.governor.enforce(self.recursive)

    def run(self):
        while True:
            rec = self.recursive.step()

            # 🛡 validate output
            rec = self.governor.validate(rec)

            agents = rec.get("agents", {})
            if not agents:
                continue

            strongest = max(agents, key=agents.get)

            print("[Ω-GOV v6]", strongest, agents[strongest], rec.get("tick"))
