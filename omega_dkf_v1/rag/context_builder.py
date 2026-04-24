def build_context(chunks):
    return " | ".join([c["text"] for c in chunks])
