class OmegaLayerGuardV78:

    @staticmethod
    def validate(layer):
        if isinstance(layer, str):
            raise Exception("[LAYER GUARD] Execution layer is STRING, expected object")

        if not hasattr(layer, "route"):
            raise Exception("[LAYER GUARD] Missing route() method")

        if not hasattr(layer, "nodes"):
            raise Exception("[LAYER GUARD] Missing nodes registry")

        return layer
