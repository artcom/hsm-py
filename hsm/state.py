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

    def add_handler(self, event, target, action=None):
        """
        Adds an event handler for state transitions

        Args:
            event (str): the name of the event
            target (State): the state tot transition to
            action (func) when not None the event will be handled by an internal transition
        """
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        handler = _EventHandler(target, action)
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


class _EventHandler:
    def __init__(self, target, action):
        self.target = target
        self.action = action
