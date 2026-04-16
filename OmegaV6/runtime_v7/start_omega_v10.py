from runtime_v7.core.omega_v10_recursive_core import OmegaV10RecursiveCore


class OmegaV10Runtime:

    def __init__(self):
        print("\n⚙️ [OMEGA V10 BOOT] STARTING SYSTEM RUNTIME...\n")

        self.core = OmegaV10RecursiveCore(node_port=6100)

        print("\n⚙️ [OMEGA V10 BOOT] SYSTEM ONLINE\n")

    def run(self):
        while True:
            try:
                user = input("\n~Omega$> ").strip()

                if user.lower() == "exit":
                    print("[OMEGA] shutting down...")
                    self.core.stop()
                    break

                self.core.emit({
                    "type": "user_input",
                    "content": user
                })

                print(f"[OMEGA] {user}")

            except KeyboardInterrupt:
                print("\n[OMEGA] interrupted")
                self.core.stop()
                break


if __name__ == "__main__":
    OmegaV10Runtime().run()
