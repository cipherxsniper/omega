from runtime_v7.core._patch_v82_bind_fix import safe_bind

def apply_bind_patch(node):
    node.port = safe_bind(node.sock, node.port)
    return node.port
