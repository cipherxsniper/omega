class CognitionRouter:
    def route(self, nodes, query):
        if not nodes:
            return []

        # simple role-based routing
        mapped = []
        for n in nodes:
            priority = 1 if n.role == "reasoner" else 0.5
            mapped.append((priority, n))

        mapped.sort(reverse=True, key=lambda x: x[0])
        return [n for _, n in mapped]
