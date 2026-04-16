class ThoughtExporterV6:
    def __init__(self, state):
        self.state = state

    def export(self):
        ideas = self.state["ideas"]

        print("\n🧠 OMEGA COGNITIVE FIELD REPORT")
        print("=" * 40)

        for k, v in ideas.items():
            strength = v.get("strength", 0)
            links = v.get("links", [])

            print(f"\nIdea: {k}")
            print(f"  Strength: {strength:.3f}")

            if links:
                print(f"  Connected To: {', '.join(links)}")
            else:
                print("  Connected To: none")

        print("\n" + "=" * 40 + "\n")
