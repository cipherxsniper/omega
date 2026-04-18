# 🧠 Omega Thought Path Tracer v11.8

from omega_message_bus_v12 import bus


class ThoughtTracer:

    def trace(self):

        messages = bus.get_messages("routing")

        chain = []

        for m in messages[-10:]:
            node = m["payload"]["node"]
            choice = m["payload"]["choice"]

            chain.append(f"{node} → {choice}")

        return " → ".join(chain)


tracer = ThoughtTracer()
