class OmegaTypeEnforcerV79:

    @staticmethod
    def enforce_layer(layer):
        if layer is None:
            raise Exception("[TYPE ERROR] layer is None")

        if isinstance(layer, str):
            raise Exception("[TYPE ERROR] layer is STRING, not execution object")

        if not hasattr(layer, "route"):
            raise Exception("[TYPE ERROR] Missing route()")

        if not hasattr(layer, "nodes"):
            raise Exception("[TYPE ERROR] Missing nodes registry")

        return layer
