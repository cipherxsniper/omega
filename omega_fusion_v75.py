class OmegaFusionV75:
    def fuse(self, field):
        nodes = field.global_memory["nodes"]

        for node_a in nodes:
            for node_b in nodes:
                if node_a == node_b:
                    continue

                a = nodes[node_a]
                b = nodes[node_b]

                if abs(a["avg_health"] - b["avg_health"]) < 0.1:
                    field.global_memory["relationships"].setdefault(node_a, []).append(node_b)
