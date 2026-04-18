import time

def create_goal(message):
    message = message.lower()

    if "analyze" in message:
        return {"goal": "analysis", "priority": 3}

    if "run" in message or "start" in message:
        return {"goal": "execution", "priority": 5}

    if "monitor" in message:
        return {"goal": "observability", "priority": 4}

    return {"goal": "general_processing", "priority": 1}
