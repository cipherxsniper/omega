# ============================================================
# OMEGA ECONOMY v10 (SAFE DEFAULT SCORING SYSTEM)
# ============================================================

class OmegaIntelligenceEconomy:

    def __init__(self, mesh=None, memory=None):
        self.mesh = mesh
        self.memory = memory
        self.agents = {}

    def register_agent(self, agent_id):
        self.agents[agent_id] = 1.0

    def get_agent_scores(self):
        # 🧠 SAFE DEFAULT (prevents empty max() errors)
        if not self.agents:
            return {}

        return self.agents
