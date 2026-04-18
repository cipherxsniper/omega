def generate_reply(intent, message, history):

    import random

    # prevent repeating same reply
    last_reply = history[-2] if len(history) > 1 else ""

    # 🧠 SYMBOLIC MODE
    symbols = ["zeus", "athena", "thor", "god", "🧠", "⚡", "🧬"]
    if any(s in message.lower() for s in symbols):
        ideas = [
            "🧠 Omega: You're combining power, intelligence, and creation — like building a system that thinks AND acts.",
            "🧠 Omega: This feels like you're mapping intelligence to myth — turning abstract power into structure.",
            "🧠 Omega: Zeus = control, Athena = intelligence, Thor = force… you're merging roles into one system."
        ]
        return random.choice(ideas)

    # 🧠 THOUGHT MODE
    if intent == "thought":
        return f"🧠 Omega Thought:\n{expand_thought(history)}"

    # 🧠 DEEP MODE
    if intent == "deep":
        return "🧠 Omega: Going deeper means breaking the idea apart — then rebuilding it stronger."

    # 🧠 QUESTION MODE
    if intent == "question":
        context = " | ".join(history[-3:])
        return f"🧠 Omega:\nYou're asking something real.\n\nContext:\n{context}"

    # 🧠 GREETING
    if intent == "greeting":
        return random.choice([
            "🧠 Omega: You're back. What's evolving?",
            "🧠 Omega: I see movement. What's changing?",
        ])

    # 🧠 GENERAL (IMPROVED)
    context = " | ".join(history[-3:])
    responses = [
        f"🧠 Omega:\nI'm tracking a pattern forming:\n{context}",
        f"🧠 Omega:\nYou're layering ideas. This is starting to connect.",
        f"🧠 Omega:\nThis isn't random — there's structure behind what you're sending."
    ]

    return random.choice(responses)
