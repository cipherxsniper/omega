# Ω MEMORY CONTRACT ENFORCER v6.2

ALLOWED_FIRST_ARG = "OmegaCoreState"

def validate_call(target, memory):
    if not hasattr(memory, "record"):
        raise TypeError("[Ω CONTRACT BREAK] memory object missing .record()")

    if memory.__class__.__name__ != ALLOWED_FIRST_ARG:
        raise TypeError(f"[Ω CONTRACT BREAK] invalid memory type: {type(memory)}")

    return True
