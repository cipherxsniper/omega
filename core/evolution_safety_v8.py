import copy

class EvolutionSafetyV8:
    """
    Prevents runaway self-modification.
    """

    def validate_mutation(self, mutation):
        # block empty patches
        if not mutation.get("payload"):
            return False

        # block destructive patterns
        if "rm -rf" in str(mutation):
            return False

        # block registry overwrite attempts
        if "node_registry" in str(mutation):
            return False

        return True
