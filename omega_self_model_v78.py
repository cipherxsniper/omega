class OmegaSelfModelV78:

    def snapshot(self, packet):
        return {
            "tick": packet["tick"],
            "node": packet["node"],
            "trace_size": len(packet["trace"])
        }

    def narrate(self, prev, curr):
        if not prev:
            return "System initialized."

        change = "node shift" if prev["node"] != curr["node"] else "stable routing"

        return f"[SELF MODEL] Tick {curr['tick']} | {change} → {curr['node']}"
