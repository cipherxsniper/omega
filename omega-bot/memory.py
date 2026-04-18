memory_store = {}

def save(user_id, message, reply):
    if user_id not in memory_store:
        memory_store[user_id] = []
    memory_store[user_id].append((message, reply))

def load(user_id):
    return memory_store.get(user_id, [])
