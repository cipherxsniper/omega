class ObserverGuardV79:

    def __init__(self, observer):
        self.observer = observer

    def narrate(self, prev, curr):
        try:
            return self.observer.narrate(prev, curr)
        except Exception as e:
            return f"[OBSERVER RECOVERY] {str(e)} | system stabilized"
