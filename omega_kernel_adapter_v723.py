class OmegaKernelAdapterV723:

    def __init__(self, kernel):
        self.kernel = kernel

    def step(self, tick, payload):

        # 🧠 normalize all known kernel interfaces
        if hasattr(self.kernel, "step"):
            return self.kernel.step(tick, payload)

        if hasattr(self.kernel, "route"):
            return self.kernel.route("temporal", payload, steps=4)

        if hasattr(self.kernel, "safe_step"):
            return self.kernel.safe_step(tick, payload)

        raise Exception("[Ω CONTRACT ERROR] No valid kernel execution method found")
