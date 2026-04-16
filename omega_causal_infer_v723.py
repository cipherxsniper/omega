class OmegaCausalInferV723:

    def score_relation(self, prev_event, curr_event):

        score = 0.0

        if prev_event.get("node") == curr_event.get("node"):
            score += 0.4

        if prev_event.get("event_type") != curr_event.get("event_type"):
            score += 0.2

        if curr_event.get("severity", 0.5) > 0.7:
            score += 0.3

        return min(1.0, score)

    def explain_chain(self, chain, memory):

        explanations = []

        for node_id in chain:

            entry = memory.nodes.get(node_id)

            if entry:
                ev = entry["event"]
                explanations.append(
                    f"{ev.get('event_type')} occurred at tick {ev.get('tick')}"
                )

        return " → ".join(explanations)
