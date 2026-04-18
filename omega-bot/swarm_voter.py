def vote(agents):
    scores = {
        "intent": 0,
        "emotion": 0,
        "structure": 0
    }

    for a in agents:
        if a["signal"] == "intent":
            scores["intent"] += 3
        elif a["signal"] == "emotion":
            scores["emotion"] += 5
        elif a["signal"] == "structure":
            scores["structure"] += 2

    winner = max(scores, key=scores.get)

    return {
        "winner": winner,
        "scores": scores
    }
