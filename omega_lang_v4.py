class OmegaLangV4:
    def __init__(self, state):
        self.state = state

    def exec(self, cmd):
        parts = cmd.split()
        if not parts:
            return

        op = parts[0]

        # 🧠 SAFE NODE CREATION
        if op == "SPAWN_NODE":
            node = parts[1]
            self.state["nodes"][node] = {"energy": 1.0}

        # 🧠 SAFE IDEA CREATION
        elif op == "CREATE_IDEA":
            idea = parts[1]
            self.state["ideas"][idea] = {
                "strength": 1.0,
                "links": []
            }

        # 🧠 SAFE LINKING (FIXED)
        elif op == "LINK":
            a, b = parts[1], parts[2]

            # auto-create missing nodes instead of crashing
            if a not in self.state["ideas"]:
                self.state["ideas"][a] = {"strength": 1.0, "links": []}

            if b not in self.state["ideas"]:
                self.state["ideas"][b] = {"strength": 1.0, "links": []}

            self.state["ideas"][a]["links"].append(b)

        # 🧠 EVOLUTION HOOK
        elif op == "MUTATE":
            idea = parts[1]
            if idea in self.state["ideas"]:
                self.state["ideas"][idea]["strength"] *= 1.05
