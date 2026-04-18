from gpt4all import GPT4All
import os

MODEL_PATH = os.path.expanduser("~/Omega/omega-bot/models")

# You must place a .gguf model inside this folder
MODEL_NAME = "mistral.gguf"  # change if needed

model = GPT4All(model_name=MODEL_NAME, model_path=MODEL_PATH)


def llm_think(user_message, history):
    """
    Local intelligence brain (NO API REQUIRED)
    """

    # Build lightweight context
    context = ""
    for m in history[-5:]:
        context += f"{m['role']}: {m['message']}\n"

    prompt = f"""
You are Omega, a structured AI assistant.

Conversation so far:
{context}

User: {user_message}
Omega:
"""

    with model.chat_session():
        response = model.generate(
            prompt,
            max_tokens=300,
            temp=0.7
        )

    return response.strip()
