from omega_cognition_contract_v78 import CognitionPacketV78

class OmegaKernelV78:

    def __init__(self, layer, bus=None):
        self.layer = layer
        self.bus = bus

    def step(self, tick, payload):
        trace = self.layer.route("temporal", payload, steps=4)

        packet = CognitionPacketV78(
            tick=tick,
            node=trace.get("final_node", "unknown"),
            state=payload,
            trace=trace if isinstance(trace, list) else [trace],
            memory=getattr(self.layer, "memory", {}),
            events=[]
        )

        return packet.to_dict()
