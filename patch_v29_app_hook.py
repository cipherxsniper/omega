from omega_v29_sync_engine import sync

def generate_reply(intent, message, history):
    node = "app_brain"

    result = sync(node, message)

    return f"""🧠 Omega v29 Active

{result}

📡 System State:
Message distributed across node mesh.
Memory updated globally.
"""
