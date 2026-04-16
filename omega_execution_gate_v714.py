class OmegaExecutionGateV714:

    def __init__(self, kernel):
        self.kernel = kernel

    def step(self, tick, payload):
        try:
            result = self.kernel.step(tick, payload)

            return {
                "ok": True,
                "data": result
            }

        except Exception as e:
            return {
                "ok": False,
                "error": str(e),
                "data": None
            }
