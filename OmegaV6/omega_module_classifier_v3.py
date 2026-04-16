import os

class OmegaModuleClassifierV3:
    """
    KEY RULE:
    NOT ALL CODE IS A SERVICE
    """

    def classify(self, filename):
        name = filename.lower()

        # KERNEL (always running core)
        if "kernel" in name:
            return "kernel"

        # SERVICES (long-running processes)
        if any(x in name for x in [
            "orchestrator",
            "engine",
            "brain",
            "swarm",
            "runtime",
            "supervisor",
            "daemon"
        ]):
            return "service"

        # DATA FILES
        if name.endswith(".json") or name.endswith(".log"):
            return "data"

        # LIBRARIES (NOT RUNNABLE)
        if any(x in name for x in [
            "graph",
            "memory",
            "parser",
            "classifier",
            "utility",
            "helper",
            "patch",
            "resolver",
            "compiler"
        ]):
            return "library"

        # DEFAULT SAFE MODE
        return "tool"
