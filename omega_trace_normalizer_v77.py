class OmegaTraceNormalizerV77:

    @staticmethod
    def normalize(trace):
        """
        Forces ALL trace formats into a single schema:
        {
            "final_node": str,
            "path": list,
            "raw": original_trace
        }
        """

        # CASE 1: dict with final_node
        if isinstance(trace, dict) and "final_node" in trace:
            return {
                "final_node": trace["final_node"],
                "path": trace.get("path", []),
                "raw": trace
            }

        # CASE 2: dict but missing final_node
        if isinstance(trace, dict):
            last_node = None
            if "trace" in trace and isinstance(trace["trace"], list) and trace["trace"]:
                last_node = trace["trace"][-1].get("node")
            return {
                "final_node": trace.get("node", last_node),
                "path": trace.get("trace", []),
                "raw": trace
            }

        # CASE 3: list trace (your current crash case)
        if isinstance(trace, list):
            if len(trace) == 0:
                return {"final_node": "unknown", "path": [], "raw": trace}

            last = trace[-1]
            if isinstance(last, dict):
                return {
                    "final_node": last.get("node", "unknown"),
                    "path": trace,
                    "raw": trace
                }

            return {
                "final_node": str(last),
                "path": trace,
                "raw": trace
            }

        # CASE 4: fallback
        return {
            "final_node": "unknown",
            "path": [],
            "raw": trace
        }
