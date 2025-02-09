from hsm.state import State


class Parallel(State):
    def __init__(self, name, *statemachines):
        """
        Creates an orthoginal region

        Args:
            name (str): the name of the state
            statemachines (list): the statemachines running in parallel
        """
        super().__init__(name)
        self.statemachines = statemachines
        for sm in self.statemachines:
            sm.container = self

    def enter(self, source, target, data):
        super().enter(source, target, data)
        for sm in self.statemachines:
            if target.has_ancestor_statemachine(sm):
                sm.enter(source, target, data)
            else:
                sm.setup(data)

    def exit(self, source, target, data):
        for sm in self.statemachines:
            sm.teardown(data)
        super().exit(source, target, data)

    def handle(self, event, data):
        handled = False
        for sm in self.statemachines:
            if sm.handle(event, data):
                handled = True
        return handled

    def active_states(self):
        states = []
        for sm in self.statemachines:
            states.extend(sm.active_states())
        return states
