def validate_brain_output(b):
    if not isinstance(b, dict):
        raise ValueError(f"Brain output must be dict, got {type(b)}")

    if "global_memory" not in b:
        raise ValueError("Missing global_memory key")

    if not isinstance(b["global_memory"], list):
        raise ValueError("global_memory must be list")

    return True
