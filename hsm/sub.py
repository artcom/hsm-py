from hsm.state import State


class Sub(State):
    def __init__(self, name, statemachine):
        super().__init__(name)
        self.statemachine = statemachine
        self.statemachine.parent = self

    def enter(self, source, target, data):
        super().enter(source, target, data)
        self.statemachine.enter(source, target, data)

    def exit(self, source, target, data):
        self.statemachine.teardown()
        super().exit(source, target, data)

    def handle(self, event, data):
        return self.statemachine.handle(event, data)
