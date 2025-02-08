from collections import deque


class Statemachine:

    def __init__(self, *states):
        """
        Creates a statemachine object

        Args:
            states (list): a list of State objects
        """
        self._states = states
        self._initial_state = self._states[0]
        self._current_state = None

        self._events = []
        self._queue = deque()
        self._event_in_progress = False

        self.container = None
        for s in states:
            s.owner = self

    def setup(self):
        """
        Starts the statemachine, enters the first state in list
        """
        self._current_state = self._initial_state
        self.enter(None, self._initial_state, None)

    def teardown(self):
        """
        Stops the statemachine, exits the current state
        """
        self.exit(self._current_state, None, None)
        self._current_state = None

    def handle_event(self, name, data=None):
        """
        Performs a transition by given event name.

        name (str): the name of the event
        data (Any): data passed to enter, exit and action functions
        """
        event = _Event(name, data)
        self._queue.append(event)

        if self._event_in_progress:
            return

        self._event_in_progress = True
        while len(self._queue) > 0:
            current_event = self._queue.popleft()
            self.handle(current_event.name, current_event.data)
        self._event_in_progress = False

    def enter(self, source, target, data):
        target_path = target.owner.path()
        target_level = len(target_path)
        this_level = len(self.path())

        if target_level < this_level:
            self._current_state = self._initial_state
        elif target_level == this_level:
            self._current_state = target
        else:
            self._current_state = target_path[this_level].container
        self._current_state.enter(source, target, data)

    def exit(self, source, target, data):
        self._current_state.exit(source, target, data)

    def switch_state(self, source, target, data):
        self._current_state.exit(source, target, data)
        self.enter(source, target, data)

    def handle(self, name, data):
        if self._current_state is None:
            return False

        if hasattr(self._current_state, 'handle') and callable(self._current_state.handle):
            if self._current_state.handle(name, data) is True:
                return True

        handlers = self._current_state.handlers_for_event(name)
        if handlers is None:
            return False

        for handler in handlers:
            transition = _Transition(
                self._current_state, handler.target, handler.action)
            if transition.perform_transition(data) is True:
                return True
        return False

    def path(self):
        path = [self]
        while (path[0].container is not None):
            path.insert(0, path[0].container.owner)
        return path

    def active_states(self):
        if self._current_state is None:
            return []

        states = [self._current_state.name]
        if hasattr(self._current_state, 'statemachine'):
            states.extend(self._current_state.statemachine.active_states())
        return states


class _Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class _Transition:
    def __init__(self, source, target, action):
        self._source = source
        self._target = target
        self._action = action

    def perform_transition(self, data):
        if self._action is not None:
            self._action(data)
        else:
            lca = self._find_lca()
            lca.switch_state(self._source, self._target, data)
        return True

    def _find_lca(self):
        source_path = self._source.owner.path()
        target_path = self._target.owner.path()
        lca = None

        for statemachine in reversed(source_path):
            if statemachine in target_path:
                lca = statemachine
                break
        return lca
