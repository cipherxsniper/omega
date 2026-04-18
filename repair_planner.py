def generate_repair_plan(graph, issues, stability):
    plan = []

    for issue in issues:
        plan.append({
            "issue": issue["type"],
            "target": issue["node"],
            "suggested_action": "create_stub_or_fix_import",
            "risk": "low",
            "approved": False
        })

    return plan
