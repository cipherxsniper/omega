from omega_event_contract_v79 import OmegaEventContractV79

class OmegaKernelV710:

    def __init__(self, layer, bus):
        self.layer = layer
        self.bus = bus

    def step(self, tick, payload):

        try:
            trace = self.layer.route("temporal", payload, steps=4)

            event = OmegaEventContractV79.build(
                event_type="trace_event",
                source="kernel",
                raw=trace,
                system_state={"tick": tick},
                severity=0.2
            )

        except Exception as e:

            event = OmegaEventContractV79.build(
                event_type="route_error",
                source="kernel",
                raw=str(e),
                system_state={"tick": tick},
                severity=1.0
            )

        return self.bus.publish(event)
