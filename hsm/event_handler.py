class EventHandler:
    def __init__(self, target, guard, action, kind):
        self.target = target
        self.guard = guard
        self.action = action
        self.kind = kind
