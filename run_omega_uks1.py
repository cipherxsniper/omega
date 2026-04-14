from system.omega_recursive_v1 import OmegaRecursiveV1
from system.omega_orchestrator_v1 import OmegaOrchestratorV1

rec = OmegaRecursiveV1()
orch = OmegaOrchestratorV1(rec)

orch.run()
