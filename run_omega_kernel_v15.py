from omega_unified_kernel_v15 import OmegaUnifiedKernelV15

# simple brain registry (can expand later)
brains = ["brain_0", "brain_1", "brain_2", "brain_3"]

kernel = OmegaUnifiedKernelV15(brains)
kernel.run()
