from planner import plan
import tools
import memory

def run(user_id, message):
    steps = plan(message)

    if "greet" in steps:
        reply = tools.greet()

    elif "identity" in steps:
        reply = tools.identity()

    elif "explain" in steps:
        reply = tools.explain(message)

    else:
        reply = tools.reflect(message)

    memory.save(user_id, message, reply)
    return reply
