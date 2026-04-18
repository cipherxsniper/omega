# 🧠 Omega v12 Message Bus (Cross-Node Communication Layer)

import json
import time
from collections import defaultdict

STATE_FILE = "omega_bus_v12.json"


class MessageBus:

    def __init__(self):
        self.subscribers = defaultdict(list)
        self.messages = []

    def subscribe(self, node, channel):
        self.subscribers[channel].append(node)

    def publish(self, channel, payload):
        msg = {
            "channel": channel,
            "payload": payload,
            "timestamp": time.time()
        }
        self.messages.append(msg)

    def get_messages(self, channel=None):
        if channel:
            return [m for m in self.messages if m["channel"] == channel]
        return self.messages


bus = MessageBus()
