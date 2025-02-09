import pytest

from hsm import State, Sub, Parallel, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    a = State("a")
    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))
    p1 = State("p1")
    p = Parallel("p", Statemachine(p1))
    sm = Statemachine(a, s, p)

    def a_internal(data):
        sequence.append("a:internal" + str(data))

    def a_enter(data):
        sequence.append("a:enter" + str(data))

    def a_exit(data):
        sequence.append("a:exit" + str(data))

    def s_enter(data):
        sequence.append("s:enter" + str(data))

    def s_exit(data):
        sequence.append("s:exit" + str(data))

    def s1_enter(data):
        sequence.append("s1:enter" + str(data))

    def s1_exit(data):
        sequence.append("s1:exit" + str(data))

    def p_enter(data):
        sequence.append("p:enter" + str(data))

    def p_exit(data):
        sequence.append("p:exit" + str(data))

    def p1_enter(data):
        sequence.append("p1:enter" + str(data))

    def p1_exit(data):
        sequence.append("p1:exit" + str(data))

    a.enter_func = a_enter
    a.exit_func = a_exit
    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    p.enter_func = p_enter
    p.exit_func = p_exit
    p1.enter_func = p1_enter
    p1.exit_func = p1_exit

    a.add_handler("Ainternal", a, action=a_internal,
                  kind=TransitionKind.INTERNAL)
    a.add_handler("AtoS", s)
    a.add_handler("AtoP", p)
    s.add_handler("StoA", a)
    p.add_handler("PtoA", a)

    sm.setup()
    yield sm


def test_data_flow(statemachine, sequence):
    sequence.clear()
    statemachine.handle_event("Ainternal", "_myData")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:internal_myData"]

    sequence.clear()
    statemachine.handle_event("AtoS", "_123")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["a:exit_123", "s:enter_123", "s1:enter_123"]

    sequence.clear()
    statemachine.handle_event("StoA", "_456")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["s1:exit_456", "s:exit_456", "a:enter_456"]

    sequence.clear()
    statemachine.handle_event("AtoP", "_789")
    assert statemachine.active_states() == ["p", "p1"]
    assert sequence == ["a:exit_789", "p:enter_789", "p1:enter_789"]

    sequence.clear()
    statemachine.handle_event("PtoA", "_abc")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["p1:exit_abc", "p:exit_abc", "a:enter_abc"]
