APPROVED_REPAIRS = set()

def approve_repair(module):
    # simple rule: allow first attempt, block loops
    if module in APPROVED_REPAIRS:
        return False

    APPROVED_REPAIRS.add(module)
    return True
