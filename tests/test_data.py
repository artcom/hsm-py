import pytest

from hsm import State, Sub, Statemachine


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    a = State("a")
    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))
    sm = Statemachine(a, s)

    a.add_handler("AtoS", s)

    def a_internal(data):
        sequence.append("a:internal" + str(data))

    a.add_handler("Ainternal", a, a_internal)

    def a_enter(data):
        sequence.append("a:enter" + str(data))

    def a_exit(data):
        sequence.append("a:exit" + str(data))

    def s_enter(data):
        sequence.append("s:enter" + str(data))

    def s1_enter(data):
        sequence.append("s1:enter" + str(data))

    a.enter_func = a_enter
    a.exit_func = a_exit
    s.enter_func = s_enter
    s1.enter_func = s1_enter

    sm.setup()
    yield sm


def test_sub_switching(statemachine, sequence):
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:enterNone"]

    sequence.clear()
    statemachine.handle_event("Ainternal", "_foobar")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:internal_foobar"]

    sequence.clear()
    statemachine.handle_event("AtoS", "_123")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["a:exit_123", "s:enter_123", "s1:enter_123"]
