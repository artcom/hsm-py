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
