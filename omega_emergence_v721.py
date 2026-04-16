class OmegaEmergenceV721:

    def detect_patterns(self, memory_field):

        patterns = {}

        for k, v in memory_field.items():

            if v["weight"] > 2.0:
                patterns[k] = "dominant"

            elif v["weight"] > 1.2:
                patterns[k] = "emerging"

        return patterns

    def summarize(self, patterns):

        dominant = [k for k, v in patterns.items() if v == "dominant"]
        emerging = [k for k, v in patterns.items() if v == "emerging"]

        return {
            "dominant_patterns": dominant,
            "emerging_patterns": emerging,
            "summary": (
                f"{len(dominant)} dominant patterns, "
                f"{len(emerging)} emerging patterns detected"
            )
        }
