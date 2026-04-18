import json
from collections import defaultdict

class NodeBrainDistributionCenter:
    """
    Omega System Operator Brain (Safe Mode)
    - Diagnoses system state
    - Clusters failures
    - Generates repair plans
    - DOES NOT execute mutations automatically
    """

    def __init__(self):
        self.issues = []
        self.clusters = defaultdict(list)
        self.repair_plan = []

    # -----------------------------
    # INPUT INGESTION
    # -----------------------------
    def ingest(self, issues):
        self.issues = issues
        return len(issues)

    # -----------------------------
    # CLUSTER ENGINE
    # -----------------------------
    def cluster_issues(self):
        for issue in self.issues:
            t = issue.get("type", "unknown")
            self.clusters[t].append(issue)

        return dict(self.clusters)

    # -----------------------------
    # ROOT CAUSE SCORING
    # -----------------------------
    def score_clusters(self):
        scored = []

        for cluster_type, items in self.clusters.items():
            score = len(items)

            scored.append({
                "cluster": cluster_type,
                "count": score,
                "severity": self._severity(score)
            })

        return sorted(scored, key=lambda x: x["count"], reverse=True)

    def _severity(self, score):
        if score > 100:
            return "CRITICAL"
        elif score > 30:
            return "HIGH"
        elif score > 10:
            return "MEDIUM"
        return "LOW"

    # -----------------------------
    # REPAIR PLANNER (NO EXECUTION)
    # -----------------------------
    def generate_repair_plan(self):
        plan = []

        for cluster, items in self.clusters.items():
            plan.append({
                "issue_type": cluster,
                "impacted_nodes": len(items),
                "suggested_action": self._suggest_action(cluster),
                "requires_approval": True
            })

        self.repair_plan = plan
        return plan

    def _suggest_action(self, cluster):
        if cluster == "parse_error":
            return "fix_syntax_or_isolate_module"
        if cluster == "import_error":
            return "repair_dependency_graph"
        if cluster == "missing_module":
            return "create_safe_stub"
        return "manual_review_required"

    # -----------------------------
    # OPERATOR OUTPUT
    # -----------------------------
    def report(self):
        return {
            "total_issues": len(self.issues),
            "clusters": self.cluster_issues(),
            "ranked_severity": self.score_clusters(),
            "repair_plan": self.generate_repair_plan(),
            "mode": "SAFE_OPERATOR_MODE"
        }


# -----------------------------
# ENTRYPOINT TEST
# -----------------------------
if __name__ == "__main__":
    brain = NodeBrainDistributionCenter()

    print("🧠 NODE BRAIN DISTRIBUTION CENTER ONLINE")

    # placeholder safe test input
    test_issues = [
        {"type": "import_error", "node": "omega_bus"},
        {"type": "missing_module", "node": "supervisor_v3"},
        {"type": "parse_error", "node": "fix_core_blocks"}
    ]

    brain.ingest(test_issues)

    report = brain.report()

    print(json.dumps(report, indent=2))
