def register(COMMANDS):
    def echo(parts):
        print("[Ω-ECHO]", " ".join(parts[1:]))

    COMMANDS["echo"] = echo
