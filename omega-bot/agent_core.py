from brains import planner, critic, memory_filter
from llm_brain import llm_think


def plan_task(user_message):
    """
    Break input into intent + strategy
    """
    intent = planner(user_message)

    if intent == "greeting":
        return ["respond_social"]

    if intent == "recall":
        return ["fetch_memory", "respond_social"]

    if intent == "reasoning":
        return ["analyze", "respond_reason"]

    return ["analyze", "respond_general"]


def execute_pipeline(steps, user_message, history):
    """
    Executes agent workflow step-by-step
    """

    memory = memory_filter(history)

    result = ""

    # 🧠 STEP 1: reasoning (LLM core)
    if "analyze" in steps:
        result = llm_think(user_message, memory)

    # 🧠 STEP 2: social formatting layer
    if "respond_social" in steps:
        result = f"Hello. I'm Omega. {user_message}"

    if "respond_reason" in steps:
        result = f"Let’s break this down: {result}"

    if "respond_general" in steps:
        result = result

    # ⚖️ FINAL SAFETY CHECK
    result = critic(result)

    return result
