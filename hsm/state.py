from hsm.transition_kind import TransitionKind


class State:
    def __init__(self, name):
        """
        Creates a state object

        Args:
            name (str): the name of the state
        """
        self._event_handlers = {}

        self.name = name
        self.owner = None
        self.enter_func = None
        self.exit_func = None

    def add_handler(self, event, target, action=None, kind=TransitionKind.EXTERNAL):
        """
        Adds an event handler for state transitions

        Args:
            event (str): the name of the event
            target (State): the state to transition to
            action (func): function to be executed on internal transition
            kind (TransitionKind): kind of transition to perform

        Raises:
            RuntimeError: when source and target are not equal for internal transitions
            RuntimeError: when no action is set for internal transition
        """
        if kind == TransitionKind.INTERNAL and self != target:
            raise RuntimeError(
                "State.addhandler: Source and target states must be equal for internal transition!")

        if kind == TransitionKind.INTERNAL and action is None:
            raise RuntimeError(
                "State.addhandler: Action must be set for internal transition!")

        if event not in self._event_handlers:
            self._event_handlers[event] = []
        handler = _EventHandler(target, action, kind)
        self._event_handlers[event].append(handler)

    def handlers_for_event(self, event):
        if event in self._event_handlers:
            return self._event_handlers[event]
        else:
            return None

    def enter(self, _, __, data):
        if self.enter_func is not None:
            self.enter_func(data)

    def exit(self, _, __, data):
        if self.exit_func is not None:
            self.exit_func(data)

    def has_ancestor(self, other):
        if self.owner.container is None:
            return False
        if self.owner.container == other:
            return True
        return self.owner.container.has_ancestor(other)


class _EventHandler:
    def __init__(self, target, action, kind):
        self.target = target
        self.action = action
        self.kind = kind
