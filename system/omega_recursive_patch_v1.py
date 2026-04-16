class StepInterfaceMixin:
    def step(self):
        if hasattr(self, "run"):
            return self.run()
        if hasattr(self, "tick"):
            return self.tick()
        raise RuntimeError("No step/run/tick method found in recursive engine")
