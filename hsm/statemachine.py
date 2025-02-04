class Statemachine:

    def __init__(self, *states):
        self.states = states
        self.initial_state = states[0]
        self.current_state = None
        self.events = []
        self.parent = None
        self.set_parent(states)

    def set_parent(self, states):
        for s in states:
            s.parent = self

    def setup(self):
        self.current_state = self.initial_state
        self.enter(None, self.initial_state, None)

    def teardown(self):
        self.exit(self.current_state, None, None)
        self.current_state = None

    def enter(self, source, target, data):
        target_level = len(target.parent.path())
        this_level = len(self.path())

        if target_level < this_level:
            self.current_state = self.initial_state
        elif target_level == this_level:
            self.current_state = target
        else:
            target_path = target.parent.path()
            node = target_path[this_level]
            self.current_state = node.parent

        self.current_state.enter(source, target, data)

    def exit(self, source, target, data):
        self.current_state.exit(source, target, data)

    def switch_state(self, source, target, data):
        self.current_state.exit(source, target, data)
        self.enter(source, target, data)

    def handle_event(self, event, data=None):
        if self.current_state is None:
            return False

        if hasattr(self.current_state, 'handle_event') and callable(self.current_state.handle_event):
            if self.current_state.handle_event(event, data) is True:
                return True

        handlers = self.current_state.handlers_for_event(event)
        if handlers is None:
            return False

        for handler in handlers:
            transition = Transition(
                self.current_state, handler.target, handler.action)
            if transition.perform_transition(data) is True:
                return True
        return False

    def path(self):
        path = []
        statemachine = self
        while (statemachine is not None):
            path.insert(0, statemachine)
            if statemachine.parent is not None:
                statemachine = statemachine.parent.parent
            else:
                statemachine = None
        return path


class Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Transition:
    def __init__(self, source, target, action):
        self.source = source
        self.target = target
        self.action = action

    def perform_transition(self, data):
        if self.action is not None:
            self.action(data)
        else:
            lca = self.find_lca()
            lca.switch_state(self.source, self.target, data)
        return True

    def find_lca(self):
        source_path = self.source.path()
        target_path = self.target.path()
        lca = None

        for e in reversed(source_path):
            if isinstance(e, Statemachine):
                if e in target_path:
                    lca = e
                    break
        return lca
