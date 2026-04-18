from omega.core.global_memory import write
from omega.core.event_bus import emit

class CognitiveValidator:
    def __init__(self):
        self.scores = {}

    def score_node(self, node_name, event_emitted, memory_written, error_count):
        """
        Cognitive Integrity Score:
        1.0 = perfect compliance
        0.0 = dead node
        """

        score = 1.0

        if not event_emitted:
            score -= 0.5

        if not memory_written:
            score -= 0.3

        score -= min(error_count * 0.1, 0.5)

        score = max(0.0, score)

        self.scores[node_name] = score

        write({
            "type": "cognitive_integrity",
            "node": node_name,
            "score": score
        })

        return score

validator = CognitiveValidator()
