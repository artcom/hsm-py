class State:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.event_handlers = {}
        self.enter_func = None
        self.exit_func = None

    def add_handler(self, event, target, action=None):
        handler = _EventHandler(event, target, action)
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def handlers_for_event(self, event):
        if event in self.event_handlers:
            return self.event_handlers[event]
        else:
            return None

    def enter(self, source, target, data):
        if self.enter_func is not None:
            self.enter_func(data)

    def exit(self, source, target, data):
        if self.exit_func is not None:
            self.exit_func(data)

    def path(self):
        path = []
        state = self
        while state is not None:
            path.insert(0, state)
            state = state.parent
        return path


class _EventHandler:
    def __init__(self, event, target, action):
        self.event = event
        self.target = target
        self.action = action
