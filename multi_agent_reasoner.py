import random

def agents_think(concept):
    agents = {
        "Structure": f"maps {concept} as system architecture",
        "Meaning": f"interprets {concept} as semantic abstraction",
        "Symbolism": f"sees {concept} as archetypal representation"
    }

    votes = {
        "Structure": random.randint(0, 50),
        "Meaning": random.randint(0, 50),
        "Symbolism": random.randint(0, 50)
    }

    winner = max(votes, key=votes.get)

    return {
        "winner": winner,
        "analysis": agents[winner],
        "votes": votes
    }
