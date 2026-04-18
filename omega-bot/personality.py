import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_profile(user_id):
    key = f"user:{user_id}:profile"
    data = r.hgetall(key)
    return data if data else {
        "tone": "neutral",
        "depth": "medium",
        "formality": "balanced",
        "messages": "0"
    }

def update_profile(user_id, message):
    key = f"user:{user_id}:profile"
    profile = get_profile(user_id)

    msg_count = int(profile.get("messages", 0)) + 1

    # crude behavior detection
    if len(message) > 120:
        profile["depth"] = "deep"
    elif len(message) < 20:
        profile["depth"] = "short"

    if any(x in message.lower() for x in ["code", "python", "node", "bug"]):
        profile["tone"] = "technical"

    elif any(x in message.lower() for x in ["feel", "think", "life", "meaning"]):
        profile["tone"] = "philosophical"

    profile["messages"] = str(msg_count)

    r.hset(key, mapping=profile)

    return profile
