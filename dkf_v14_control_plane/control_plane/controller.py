from control_plane.process_manager import ProcessManager
from control_plane.input_router import InputRouter
from control_plane.state import DKFState

class ControlPlane:
    def __init__(self):
        self.state = DKFState()
        self.pm = ProcessManager(self.state)
        self.router = InputRouter(self.pm, self.state)

    def start(self):
        print("🧠 DKF v14 CONTROL PLANE ONLINE")
        print("⚡ Single runtime | Process-safe | No tmux mode")

        self.pm.bootstrap()

        while True:
            try:
                user_input = input("DKF > ")
                self.router.handle(user_input)

            except KeyboardInterrupt:
                print("\n🛑 Shutdown signal received")
                self.pm.shutdown_all()
                break
