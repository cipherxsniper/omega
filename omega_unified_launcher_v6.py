from system.omega_orchestrator_v9_governed import GovernedOrchestrator
from system.omega_recursive_intelligence_v13 import OmegaRecursiveIntelligenceV13

print("[Ω-v6] Booting Governance Layer...")

engine = OmegaRecursiveIntelligenceV13()
core = GovernedOrchestrator(engine)

core.run()
