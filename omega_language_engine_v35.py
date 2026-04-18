def generate_sentence(context, memory):
    """
    Converts node activity into structured English meaning.
    """

    recent = memory[-3:] if memory else []

    return f"""
🧠 Omega Interpretation:

Current Context:
{context}

Recent Memory Patterns:
{recent}

Meaning:
The system is forming relationships between distributed cognitive nodes.

Reflection:
What is the system trying to stabilize across time?

Question:
What should this system become next?
"""
