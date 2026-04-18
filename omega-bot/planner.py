def plan(user_message: str):
    msg = user_message.lower()

    steps = []

    if "hello" in msg or "hi" in msg:
        steps.append("greet")

    elif "who are you" in msg:
        steps.append("identity")

    elif "what" in msg or "explain" in msg:
        steps.append("explain")

    else:
        steps.append("reflect")

    return steps
