import pytest

from hsm import State, Sub, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    s11 = State("s11")
    s12 = State("s12")
    s1 = Sub('s1', Statemachine(s11, s12))
    s = Sub('s', Statemachine(s1))
    sm = Statemachine(s)

    def s_enter(_):
        sequence.append("s:enter")

    def s_exit(_):
        sequence.append("s:exit")

    def s1_enter(_):
        sequence.append("s1:enter")

    def s1_exit(_):
        sequence.append("s1:exit")

    def s11_enter(_):
        sequence.append("s11:enter")

    def s11_exit(_):
        sequence.append("s11:exit")

    def s12_enter(_):
        sequence.append("s12:enter")

    def s12_exit(_):
        sequence.append("s12:exit")

    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    s11.enter_func = s11_enter
    s11.exit_func = s11_exit
    s12.enter_func = s12_enter
    s12.exit_func = s12_exit

    s11.add_handler("initial", s12)
    s12.add_handler("local_down", s1, kind=TransitionKind.LOCAL)
    s1.add_handler("local_up", s12, kind=TransitionKind.LOCAL)
    s12.add_handler("local_down_double", s, kind=TransitionKind.LOCAL)
    s.add_handler("local_up_double", s12, kind=TransitionKind.LOCAL)

    sm.setup()
    yield sm


def test_local_transitions_one_level(statemachine, sequence):
    statemachine.handle_event("initial")

    sequence.clear()
    statemachine.handle_event("local_down")
    assert statemachine.active_states() == ["s", "s1", "s11"]
    assert sequence == ["s12:exit", "s11:enter"]

    sequence.clear()
    statemachine.handle_event("local_up")
    assert statemachine.active_states() == ["s", "s1", "s12"]
    assert sequence == ["s11:exit", "s12:enter"]


def test_local_transitions_two_levels(statemachine, sequence):
    statemachine.handle_event("initial")

    sequence.clear()
    statemachine.handle_event("local_down_double")
    assert statemachine.active_states() == ["s", "s1", "s11"]
    assert sequence == ["s12:exit", "s1:exit", "s1:enter", "s11:enter"]

    sequence.clear()
    statemachine.handle_event("local_up_double")
    assert statemachine.active_states() == ["s", "s1", "s12"]
    assert sequence == ["s11:exit", "s1:exit", "s1:enter", "s12:enter"]
