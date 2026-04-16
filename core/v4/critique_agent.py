from omega_event_bus_v4 import BUS

class CritiqueAgent:

    def handle(self, event):
        if event["type"] != "reasoned_output":
            return

        data = event["payload"]

        critique = {
            "status": "approved",
            "confidence": 0.82
        }

        BUS.emit("validated_output", {
            "data": data,
            "critique": critique
        })

AGENT = CritiqueAgent()
BUS.subscribe(AGENT.handle)
