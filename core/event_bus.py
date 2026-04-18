# OMEGA EVENT BUS v1

GLOBAL_BUS = []

def emit(event):
    GLOBAL_BUS.append(event)

def read(n=50):
    return GLOBAL_BUS[-n:]
