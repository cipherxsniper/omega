from system.omega_governance_v7 import OmegaGovernanceV7

class PatchedOrchestratorMixin:
    def apply_governance(self, rec):
        gov = OmegaGovernanceV7()
        return gov.normalize_output(rec)

    def safe_recursive_step(self):
        gov = OmegaGovernanceV7()

        try:
            rec = self.recursive.step()
        except Exception:
            rec = {
                "agents": {"brain_0": 1.0},
                "metrics": {"recovered": True},
                "meta": {"error_recovery": True}
            }

        rec = gov.normalize_output(rec)
        return rec
