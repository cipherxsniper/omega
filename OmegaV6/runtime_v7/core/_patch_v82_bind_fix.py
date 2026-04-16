# PATCH: safe bind wrapper

import socket

def safe_bind(sock, port):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("0.0.0.0", port))
        return port
    except OSError:
        # fallback dynamic port
        sock.bind(("0.0.0.0", 0))
        return sock.getsockname()[1]
