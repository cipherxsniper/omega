memory = {}

def add(user_id, message, reply):
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(f"U:{message} | A:{reply}")

    # compress if too large
    if len(memory[user_id]) > 8:
        memory[user_id] = [compress(memory[user_id])]

def compress(history):
    # simple semantic compression (no LLM needed)
    summary = " | ".join(history[-3:])
    return f"[COMPRESSED MEMORY] {summary}"

def get(user_id):
    return memory.get(user_id, [])
