from hsm.event_handler import EventHandler


class State:
    def __init__(self, name):
        self.parent = None
        self.name = name
        self.event_handlers = {}

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
        print(self.name + " enter")

    def exit(self, source, target):
        print(self.name + " exit")

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
