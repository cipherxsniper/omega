class OmegaCausalMemoryV723:

    def __init__(self):
        self.nodes = {}   # event_id → event
        self.edges = []   # (cause → effect)

    def add_event(self, event):

        eid = f"{event.get('tick')}_{event.get('event_type')}"

        self.nodes[eid] = {
            "event": event,
            "strength": event.get("severity", 0.5)
        }

        return eid

    def link(self, cause_id, effect_id, confidence=0.5):

        self.edges.append({
            "cause": cause_id,
            "effect": effect_id,
            "confidence": confidence
        })

    def infer_cause(self, event_id):

        causes = []

        for e in self.edges:
            if e["effect"] == event_id:
                causes.append((e["cause"], e["confidence"]))

        causes.sort(key=lambda x: x[1], reverse=True)

        return causes[:3]

    def trace_back(self, event_id):

        chain = [event_id]
        current = event_id

        for _ in range(3):

            causes = self.infer_cause(current)

            if not causes:
                break

            current = causes[0][0]
            chain.append(current)

        return chain
