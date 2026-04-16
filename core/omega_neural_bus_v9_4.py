# Nexus v9.6 event bus shim (compat layer)

BUS = {}

def subscribe(channel, handler):
    BUS.setdefault(channel, []).append(handler)

def publish(channel, message):
    for handler in BUS.get(channel, []):
        try:
            handler(message)
        except Exception as e:
            print("[BUS ERROR]", e)
