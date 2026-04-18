from omega_v33_main_brain import brain

def handle_input(message):
    return brain.process(message)

def system_boot():
    return brain.boot()

def heartbeat():
    return brain.heartbeat_all()
