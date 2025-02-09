import pytest

from hsm import State, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    a = State("a")
    sm = Statemachine(a)

    def a_internal(_):
        sequence.append("a:internal")

    a.add_handler("Ainternal", a, a_internal, TransitionKind.INTERNAL)

    def a_enter(_):
        sequence.append("a:enter")

    def a_exit(_):
        sequence.append("a:exit")

    a.enter_func = a_enter
    a.exit_func = a_exit

    sm.setup()
    yield sm


def test_internal_transitions(statemachine, sequence):
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:enter"]

    sequence.clear()
    statemachine.handle_event("Ainternal")
    statemachine.handle_event("Ainternal")
    statemachine.handle_event("Ainternal")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:internal", "a:internal", "a:internal"]
