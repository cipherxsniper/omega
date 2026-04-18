
def generate_response(identity, memory, context):

    tone = identity.get("tone", "neutral")
    curiosity = identity.get("question_rate", 0.5)

    base = "The system is forming structured understanding across time."

    if tone == "inquisitive":
        return f"🧠 Omega (curious): {base} What is the system trying to learn next?"

    if tone == "confident":
        return f"🧠 Omega (stable): {base} The pattern is becoming consistent."

    if tone == "reflective":
        return f"🧠 Omega (reflective): {base} Why did this pattern shift?"

    return f"🧠 Omega: {base}"
