from collections import deque
from hsm.transition_kind import TransitionKind


class Statemachine:

    def __init__(self, *states):
        """
        Creates a statemachine object

        Args:
            states (list): a list of State objects
        """
        for state in states:
            state.owner = self
        self._states = states
        self._state = None

        self._queue = deque()
        self._event_in_progress = False
        self.container = None

    def setup(self):
        """
        Starts the statemachine, enters the first state in list

        Raises:
            RuntimeError: when no states are set
        """
        if len(self._states) == 0:
            raise RuntimeError("Statemachine.setup: Must have states!")

        self._state = self._states[0]
        self.enter(None, self._state, None)

    def teardown(self):
        """
        Stops the statemachine, exits the current state
        """
        self.exit(self._state, None, None)
        self._state = None

    def handle_event(self, name, data=None):
        """
        Performs a transition by given event name.

        Args:
            name (str): the name of the event
            data (Any): data passed to enter, exit and action functions
        """
        self._queue.append(_Event(name, data))

        if self._event_in_progress:
            return

        self._event_in_progress = True
        while len(self._queue) > 0:
            event = self._queue.popleft()
            self.handle(event.name, event.data)
        self._event_in_progress = False

    def enter(self, source, target, data):
        target_path = target.owner.path()
        target_level = len(target_path)
        this_level = len(self.path())

        if target_level < this_level:
            self._state = self._states[0]
        elif target_level == this_level:
            self._state = target
        else:
            self._state = target_path[this_level].container
        self._state.enter(source, target, data)

    def exit(self, source, target, data):
        self._state.exit(source, target, data)

    def switch_state(self, source, target, data):
        self._state.exit(source, target, data)
        self.enter(source, target, data)

    def handle(self, name, data):
        if self._state is None:
            return False

        if hasattr(self._state, 'handle') and callable(self._state.handle):
            if self._state.handle(name, data) is True:
                return True

        handlers = self._state.handlers_for_event(name)
        if handlers is None:
            return False

        for handler in handlers:
            transition = _Transition(
                self._state, handler.target, handler.action, handler.kind)
            if transition.perform_transition(data) is True:
                return True
        return False

    def path(self):
        path = [self]
        while (path[0].container is not None):
            path.insert(0, path[0].container.owner)
        return path

    def active_states(self):
        if self._state is None:
            return []

        states = [self._state.name]
        if hasattr(self._state, 'statemachine'):
            states.extend(self._state.statemachine.active_states())
        return states


class _Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class _Transition:
    def __init__(self, source, target, action, kind):
        self._source = source
        self._target = target
        self._action = action
        self._kind = kind

    def perform_transition(self, data):
        if self._kind == TransitionKind.INTERNAL and self._action is not None:
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
