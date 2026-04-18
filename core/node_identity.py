import socket
import uuid

def get_node_id():
    return f"{socket.gethostname()}_{uuid.uuid4().hex[:6]}"
