from collections import deque

from hsm.state import EventHandler
from hsm.state import State
from hsm.transition_kind import TransitionKind


class Statemachine:

    def __init__(self, *states: State):
        """
        Creates a statemachine object

        Args:
            states (list:State): a list of State objects
        """
        for state in states:
            state.owner = self
        self._states = states

        self._queue = deque()
        self._event_in_progress = False

        self.state = None
        self.container = None

    def setup(self, data: any = None) -> None:
        """
        Starts the statemachine, enters the first state in list

        Args:
            data (any): data passed to enter, exit and action functions. Can be None.

        Raises:
            RuntimeError: when no states are set
        """
        if len(self._states) == 0:
            raise RuntimeError("Statemachine.setup: Must have states!")

        self.state = self._states[0]
        self.enter(None, self.state, data)

    def teardown(self, data: any = None) -> None:
        """
        Stops the statemachine, exits the current state

        Args:
            data (any): data passed to enter, exit and action functions. Can be None.
        """
        self.exit(self.state, None, data)
        self.state = None

    def handle_event(self, name: str, data: any = None) -> None:
        """
        Performs a transition by given event name.

        Args:
            name (str): the name of the event
            data (any): data passed to enter, exit and action functions. Can be None.
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
            self.state = self._states[0]
        elif target_level == this_level:
            self.state = target
        else:
            self.state = target_path[this_level].container
        self.state.enter(source, target, data)

    def exit(self, source, target, data):
        self.state.exit(source, target, data)

    def switch_state(self, source, target, data):
        self.state.exit(source, target, data)
        self.enter(source, target, data)

    def handle(self, name, data):
        if self.state is None:
            return False

        if hasattr(self.state, 'handle') and callable(self.state.handle):
            if self.state.handle(name, data) is True:
                return True

        handlers: EventHandler = self.state.handlers_for_event(name)
        if handlers is None:
            return False

        for handler in handlers:
            transition = _Transition(
                self.state, handler.target, handler.guard, handler.action, handler.kind)
            if transition.perform_transition(data) is True:
                return True
        return False

    def path(self):
        path = [self]
        while (path[0].container is not None):
            path.insert(0, path[0].container.owner)
        return path

    def active_states(self):
        if self.state is None:
            return []

        states = [self.state.name]
        if hasattr(self.state, 'active_states') and callable(self.state.active_states):
            states.extend(self.state.active_states())
        return states


class _Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class _Transition:
    def __init__(self, source, target, guard, action, kind):
        self._source = source
        self._target = target
        self._guard = guard
        self._action = action
        self._kind = kind

    def perform_transition(self, data):
        if not self._can_perform_transition(data):
            return False

        match self._kind:
            case TransitionKind.EXTERNAL:
                return self._perform_external_transition(data)
            case TransitionKind.INTERNAL:
                return self._perform_internal_transition(data)
            case TransitionKind.LOCAL:
                return self._perform_local_transition(data)
            case _:
                return False

    def _can_perform_transition(self, data):
        return self._guard is None or self._guard(data)

    def _perform_external_transition(self, data):
        lca = self._find_lca()
        lca.switch_state(self._source, self._target, data)
        return True

    def _perform_internal_transition(self, data):
        if self._action is not None:
            self._action(data)
        return True

    def _perform_local_transition(self, data):
        if not self._source.has_ancestor(self._target) and not self._target.has_ancestor(self._source):
            return False

        lca = self._find_lca()
        lca = lca.state.statemachine
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
