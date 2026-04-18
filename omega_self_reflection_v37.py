
class SelfReflection:

    def reflect(self, identity, memory):
        recent = memory[-5:] if memory else []

        return {
            "question": "Why did I respond the way I did?",
            "identity_state": identity,
            "pattern_check": recent,
            "hypothesis": "Behavior is emerging from repeated input patterns across time."
        }
