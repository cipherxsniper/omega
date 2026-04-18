def detect_intent(text):
    t = text.lower()

    if "what" in t and "mean" in t:
        return "clarify"
    if "why" in t:
        return "reason"
    if "who are you" in t:
        return "identity"
    if "hello" in t:
        return "greeting"
    return "general"
