from hsm.event_handler import EventHandler


class State:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.event_handlers = {}
        self.enter_func = None
        self.exit_func = None

    def add_handler(self, event, target):
        handler = EventHandler(event, target)
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def handlers_for_event(self, event):
        if event in self.event_handlers:
            return self.event_handlers[event]
        else:
            return None

    def enter(self, source, target):
        if self.enter_func is not None:
            self.enter_func()

    def exit(self, source, target):
        if self.exit_func is not None:
            self.exit_func()

    def path(self):
        path = []
        state = self
        while state is not None:
            path.insert(0, state)
            state = state.parent
        return path


class Sub(State):
    def __init__(self, name, statemachine):
        super().__init__(name)
        self.statemachine = statemachine
        self.statemachine.parent = self

    def enter(self, source, target):
        super().enter(source, target)
        self.statemachine.enter(source, target)

    def exit(self, source, target):
        self.statemachine.teardown()
        super().exit(source, target)

    def handle_event(self, event):
        return self.statemachine.handle_event(event)
