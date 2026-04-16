class OmegaMeshBusV720:

    def __init__(self):
        self.links = {}

    def connect(self, a, b):
        self.links.setdefault(a, []).append(b)

    def broadcast(self, nodes, event):
        outputs = []

        for node in nodes:
            targets = self.links.get(node.node_id, [])

            for t in targets:
                outputs.append({
                    "from": node.node_id,
                    "to": t,
                    "event": event
                })

        return outputs
