def translate(event_type, module_name="unknown", action_taken="observe"):
    return f"""
[Ω INTELLIGENCE FEED]
Event: {event_type}
Module: {module_name}
Action: {action_taken}
System State: stable
Goal: maintain coherence
"""
