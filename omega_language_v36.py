def generate_insight(memory, context):

    recent = memory[-3:] if memory else []

    return f"""
🧠 Omega Cognitive Output:

Context Stream:
{context}

Memory Trace:
{recent}

Interpretation:
The system is forming a probabilistic structure across distributed nodes.

Emergent Behavior:
Patterns are stabilizing into repeated relationships across time.

Question:
What should be strengthened in this system next?
"""
