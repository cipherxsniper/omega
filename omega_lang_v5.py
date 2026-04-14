class OmegaLangV5:
    def __init__(self, state):
        self.state = state

    def exec(self, cmd):
        p = cmd.split()
        if not p:
            return

        op = p[0]

        if op == "IDEA":
            self.state["ideas"][p[1]] = {"strength": 1.0, "fitness": 0}

        elif op == "LINK":
            a, b = p[1], p[2]

            if a not in self.state["ideas"]:
                self.state["ideas"][a] = {"strength": 1.0, "fitness": 0}

            if b not in self.state["ideas"]:
                self.state["ideas"][b] = {"strength": 1.0, "fitness": 0}

            self.state["ideas"][a]["link"] = b
