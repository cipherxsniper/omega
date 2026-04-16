from omega_ucp_v79 import UCPV79

class OmegaKernelV79:

    def __init__(self, layer):
        self.layer = layer

    def safe_step(self, tick, payload):
        try:
            trace = self.layer.route("temporal", payload, 4)

            packet = UCPV79.build(
                tick=tick,
                node=trace.get("final_node", "unknown"),
                trace=trace if isinstance(trace, list) else [trace],
                state={"ok": True},
                memory=getattr(self.layer, "memory", {}),
                events=[]
            )

            UCPV79.validate(packet)
            return packet

        except Exception as e:
            return {
                "tick": tick,
                "node": "RECOVERY_NODE",
                "trace": [],
                "state": {"recovered": True, "error": str(e)},
                "memory": getattr(self.layer, "memory", {}),
                "events": ["self_heal_triggered"]
            }
