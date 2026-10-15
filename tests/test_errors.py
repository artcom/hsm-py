import pytest

from hsm import State, Statemachine, TransitionKind


def test_no_states():
    sm = Statemachine()

    with pytest.raises(RuntimeError) as excinfo:
        sm.setup()
    assert str(excinfo.value) == "Statemachine.setup: Must have states!"


def test_internal_transitions_not_same_state():
    a = State("a")
    b = State("b")

    with pytest.raises(RuntimeError) as excinfo:
        a.add_handler("test", b, kind=TransitionKind.INTERNAL)
    assert str(
        excinfo.value) == "State.addhandler: Source and target states must be equal for internal transition!"


def test_internal_transitions_no_action():
    a = State("a")

    with pytest.raises(RuntimeError) as excinfo:
        a.add_handler("test", a, None, kind=TransitionKind.INTERNAL)
    assert str(
        excinfo.value) == "State.addhandler: Action must be set for internal transition!"


def test_setup():
    a = State("a")
    s = Statemachine(a)
    s.setup()
    s.setup()


def test_teardown():
    a = State("a")
    s = Statemachine(a)
    s.teardown()


def test_exception_in_enter_does_not_freeze_the_statemachine():
    a = State("a")
    b = State("b")
    c = State("c")

    def b_enter(_):
        raise ValueError("boom")

    b.enter_func = b_enter

    a.add_handler("toB", b)
    b.add_handler("toC", c)
    a.add_handler("toC", c)

    sm = Statemachine(a, b, c)
    sm.setup()

    with pytest.raises(ValueError):
        sm.handle_event("toB")

    assert sm._event_in_progress is False  # pylint: disable=protected-access
    assert len(sm._queue) == 0  # pylint: disable=protected-access

    # the statemachine must still process events after the exception
    sm.handle_event("toC")
    assert sm.active_states() == ["c"]
