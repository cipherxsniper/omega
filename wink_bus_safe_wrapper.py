from omega_mesh_bus_v1 import publish as _publish

def publish(node, message, state=None, signal=None):
    # auto-fill missing values safely
    if state is None:
        state = "UNKNOWN"
    if signal is None:
        signal = 0.5

    _publish(node, message, state, signal)
