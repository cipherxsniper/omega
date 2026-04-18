def planner(user_message):
    msg = user_message.lower()

    if any(x in msg for x in ["hello", "hi", "hey"]):
        return "greeting"

    if "what did i say" in msg:
        return "recall"

    if "why" in msg:
        return "reasoning"

    return "general"


def personality_brain(text):
    return f"🧠 Omega: {text}"


def critic(response):
    # prevent looping garbage
    if not response:
        return "🧠 Omega: I need more input."

    if response.count("Omega") > 3:
        return "🧠 Omega: Let’s reset the conversation. What do you want to focus on?"

    return response


def memory_filter(history):
    return history[-6:]
