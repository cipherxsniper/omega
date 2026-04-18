import random

AGENTS = ["reasoner", "critic", "optimizer"]

def vote(proposal):
    votes = {}

    for a in AGENTS:
        # simulate reasoning outcome
        votes[a] = random.choice(["APPROVE", "REJECT"])

    approve_count = list(votes.values()).count("APPROVE")

    decision = "APPROVED" if approve_count >= 2 else "REJECTED"

    return {
        "votes": votes,
        "decision": decision
    }
