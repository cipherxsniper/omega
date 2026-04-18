from agent_core import plan_task, execute_pipeline


def think(user_message, history):

    # 🧠 STEP 1: PLAN
    steps = plan_task(user_message)

    # 🧠 STEP 2: EXECUTE
    response = execute_pipeline(steps, user_message, history)

    return response, {"steps": steps}
