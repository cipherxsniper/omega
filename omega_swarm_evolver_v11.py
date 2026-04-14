# ============================================================
# OMEGA SWARM EVOLVER v11
# SELF-EXPANDING NODE + INTELLIGENCE EVOLUTION ENGINE
# ============================================================

class OmegaSwarmEvolver:
    def __init__(self, factory, economy, mesh):
        self.factory = factory
        self.economy = economy
        self.mesh = mesh

    # --------------------------------------------------------
    # EVALUATE SYSTEM NEED
    # --------------------------------------------------------

    def evaluate_growth_need(self, complexity_score):
        return complexity_score > 0.7

    # --------------------------------------------------------
    # SPAWN NEW INTELLIGENCE NODE
    # --------------------------------------------------------

    def evolve(self, complexity_score):
        if self.evaluate_growth_need(complexity_score):
            new_brain = self.factory.spawn_brain(
                purpose="auto_generated_specialist"
            )

            self.economy.register_agent(new_brain["id"])

            self.mesh.publish(
                "swarm_evolution",
                data=new_brain,
                source="swarm_evolver"
            )

            return new_brain
