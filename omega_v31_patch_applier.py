from omega_v31_consensus_engine import vote
import json
import os

def apply_proposal(proposal):
    result = vote(proposal)

    if result["decision"] != "APPROVED":
        return f"🛑 REJECTED by governance: {result['votes']}"

    path = proposal["target"]

    if not os.path.exists(path):
        return "⚠️ Target file not found"

    with open(path, "a") as f:
        f.write("\n# Omega v31 APPLIED PATCH:\n")
        f.write(str(proposal["change"]) + "\n")

    return f"✅ APPLIED: {proposal['id']} with votes {result['votes']}"
