def synthesize(nodes, memory, intent):
    context = " | ".join(nodes[-5:])

    return f"""
🧠 Omega Structured Output:

Interpretation:
The system is processing a distributed cognitive graph.

Active Nodes:
{context}

Memory State:
{memory[-3:] if isinstance(memory, list) else memory}

Inference:
The system is forming a unified semantic relationship between inputs.

Intent:
{intent}

Generated Thought:
Information is not isolated — it is continuously transforming across connected nodes.
"""
