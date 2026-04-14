# ============================================================
# OMEGA META BRAIN v10 (SAFE MODE PATCHED)
# Prevents empty evaluation crashes
# ============================================================

class OmegaMetaBrain:

    def __init__(self, economy, mesh):
        self.economy = economy
        self.mesh = mesh

    def evaluate_swarm(self):
        # Simulated matrix (replace with real metrics later)
        matrix = self.economy.get_agent_scores() if hasattr(self.economy, "get_agent_scores") else {}

        # 🛡️ SAFE GUARD (FIXES YOUR CRASH)
        if not matrix:
            return {
                "status": "warming_up",
                "message": "No swarm data yet",
                "strongest": None
            }

        strongest = max(matrix, key=matrix.get)

        return {
            "status": "active",
            "strongest": strongest,
            "score": matrix[strongest]
        }

    def rebalance(self):
        # safe no-op for now
        return True
