class OmegaObserverV78:

    def narrate(self, packet):
        return (
            f"[Ω v7.8 COGNITION REPORT]\n"
            f"Tick: {packet['tick']}\n"
            f"Active Node: {packet['node']}\n"
            f"Trace Length: {len(packet['trace'])}\n"
            f"Memory Keys: {len(packet['memory'])}\n"
        )
