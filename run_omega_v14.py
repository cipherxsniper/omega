from omega_adaptive_convergence_v14 import OmegaAdaptiveConvergenceV14

brains = ["brain_0", "brain_1", "brain_2", "brain_3"]

core = OmegaAdaptiveConvergenceV14(brains)

print("[OMEGA v14] ONLINE")

while True:
    print(core.step())

# OPTIMIZED BY v29 ENGINE
