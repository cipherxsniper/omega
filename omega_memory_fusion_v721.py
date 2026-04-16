class OmegaMemoryFusionV721:

    def __init__(self):
        self.field = {}

    def write(self, node_id, key, value):

        if key not in self.field:
            self.field[key] = {
                "value": value,
                "weight": 1.0,
                "sources": set()
            }

        entry = self.field[key]

        entry["weight"] += 0.1
        entry["value"] = value
        entry["sources"].add(node_id)

    def read(self, key):

        return self.field.get(key, None)

    def decay(self):

        to_delete = []

        for k, v in self.field.items():
            v["weight"] *= 0.97

            if v["weight"] < 0.2:
                to_delete.append(k)

        for k in to_delete:
            del self.field[k]
