from hsm.state import State
from hsm.statemachine import Statemachine


class Sub(State):
    def __init__(self, name: str, statemachine: Statemachine):
        """
        Creates a nested state object

        Args:
            name (str): the name of the state
            statemachine (Statemachine): the statemachine containing the nested state objects
        """
        super().__init__(name)
        self.statemachine = statemachine
        self.statemachine.container = self

    def enter(self, source, target, data):
        super().enter(source, target, data)
        self.statemachine.enter(source, target, data)

    def exit(self, source, target, data):
        self.statemachine.teardown(data)
        super().exit(source, target, data)

    def handle(self, event, data):
        return self.statemachine.handle(event, data)

    def active_states(self):
        return self.statemachine.active_states()
