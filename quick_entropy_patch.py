def apply_entropy_patch(kernel):
    # Safety guard
    if not hasattr(kernel, "entropy") or not hasattr(kernel, "policy"):
        return kernel

    # 🔒 Entropy regulator
    if kernel.entropy > 0.85:
        kernel.policy["exploration_bias"] *= 0.9
        kernel.policy["stability_bias"] *= 1.1

    # Clamp entropy
    kernel.entropy = min(kernel.entropy, 0.9)

    return kernel
