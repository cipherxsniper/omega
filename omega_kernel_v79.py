from omega_event_contract_v79 import OmegaEventContractV79

class OmegaKernelV79:

    def __init__(self, layer):
        self.layer = layer

    def safe_step(self, tick, payload):

        try:
            trace = self.layer.route("temporal", payload, steps=4)

            event = OmegaEventContractV79.build(
                event_type="success",
                source="kernel",
                raw=trace,
                system_state={"tick": tick},
                severity=0.1
            )

            return event

        except Exception as e:

            return OmegaEventContractV79.build(
                event_type="route_error",
                source="kernel",
                raw=str(e),
                system_state={"tick": tick},
                severity=0.9
            )
