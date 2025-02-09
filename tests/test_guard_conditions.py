import pytest

from hsm import State, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    a = State("a")
    b = State("b")
    sm = Statemachine(a, b)

    a.add_handler("AtoA", a)

    def a_internal(_):
        sequence.append("a:internal")

    def a_enter(_):
        sequence.append("a:enter")

    def a_exit(_):
        sequence.append("a:exit")

    def b_enter(_):
        sequence.append("b:enter")

    def b_exit(_):
        sequence.append("b:exit")

    a.enter_func = a_enter
    a.exit_func = a_exit
    b.enter_func = b_enter
    b.exit_func = b_exit

    def blocked(_):
        return False

    def allowed(_):
        return True

    a.add_handler("A_internal_blocked", a, action=a_internal,
                  kind=TransitionKind.INTERNAL, guard=blocked)

    a.add_handler("A_internal_allowed", a, action=a_internal,
                  kind=TransitionKind.INTERNAL, guard=allowed)

    a.add_handler("A_external_blocked", b, guard=blocked)
    a.add_handler("A_external_allowed", b, guard=allowed)

    sm.setup()
    yield sm


def test_external_transitions(statemachine, sequence):
    sequence.clear()
    statemachine.handle_event("A_internal_blocked")
    assert statemachine.active_states() == ["a"]
    assert sequence == []

    sequence.clear()
    statemachine.handle_event("A_internal_allowed")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:internal"]

    sequence.clear()
    statemachine.handle_event("A_external_blocked")
    assert statemachine.active_states() == ["a"]
    assert sequence == []

    sequence.clear()
    statemachine.handle_event("A_external_allowed")
    assert statemachine.active_states() == ["b"]
    assert sequence == ["a:exit", "b:enter"]
