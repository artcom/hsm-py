import pytest

from hsm import State, Sub, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine_external")
def statemachine_fixture_external(sequence):
    a = State("a")
    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))
    t1 = State("t1")
    t2 = State("t2")
    t = Sub('t', Statemachine(t1, t2))
    sm = Statemachine(a, s, t)

    a.add_handler("AtoA", a)
    a.add_handler("AtoS", s)
    a.add_handler("AtoS2", s2)
    s2.add_handler("S2toS2", s2)
    s.add_handler("StoA", a)
    s1.add_handler("S1toS2", s2)
    s1.add_handler("S1toS", s)
    s2.add_handler("S2toS1", s1)
    s2.add_handler("S2toT1", t1)
    t1.add_handler("T1toS1", s1)

    def a_internal(_):
        sequence.append("a:internal")

    a.add_handler("Ainternal", a, a_internal, TransitionKind.INTERNAL)

    def a_enter(_):
        sequence.append("a:enter")

    def a_exit(_):
        sequence.append("a:exit")

    def s_enter(_):
        sequence.append("s:enter")

    def s_exit(_):
        sequence.append("s:exit")

    def s1_enter(_):
        sequence.append("s1:enter")

    def s1_exit(_):
        sequence.append("s1:exit")

    def s2_enter(_):
        sequence.append("s2:enter")

    def s2_exit(_):
        sequence.append("s2:exit")

    def t_enter(_):
        sequence.append("t:enter")

    def t_exit(_):
        sequence.append("t:exit")

    def t1_enter(_):
        sequence.append("t1:enter")

    def t1_exit(_):
        sequence.append("t1:exit")

    def t2_enter(_):
        sequence.append("t2:enter")

    def t2_exit(_):
        sequence.append("t2:exit")

    a.enter_func = a_enter
    a.exit_func = a_exit
    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    s2.enter_func = s2_enter
    s2.exit_func = s2_exit
    t.enter_func = t_enter
    t.exit_func = t_exit
    t1.enter_func = t1_enter
    t1.exit_func = t1_exit
    t2.enter_func = t2_enter
    t2.exit_func = t2_exit

    sm.setup()
    yield sm


def test_external_transitions(statemachine_external, sequence):
    sequence.clear()
    statemachine_external.handle_event("AtoA")
    assert statemachine_external.active_states() == ["a"]
    assert sequence == ["a:exit", "a:enter"]

    sequence.clear()
    statemachine_external.handle_event("AtoS")
    assert statemachine_external.active_states() == ["s", "s1"]
    assert sequence == ["a:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine_external.handle_event("S1toS")
    assert statemachine_external.active_states() == ["s", "s1"]
    assert sequence == ["s1:exit", "s:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine_external.handle_event("S1toS2")
    assert statemachine_external.active_states() == ["s", "s2"]
    assert sequence == ["s1:exit", "s2:enter"]

    sequence.clear()
    statemachine_external.handle_event("S2toS2")
    assert statemachine_external.active_states() == ["s", "s2"]
    assert sequence == ["s2:exit", "s2:enter"]

    sequence.clear()
    statemachine_external.handle_event("S2toS1")
    assert statemachine_external.active_states() == ["s", "s1"]
    assert sequence == ["s2:exit", "s1:enter"]

    sequence.clear()
    statemachine_external.handle_event("StoA")
    assert statemachine_external.active_states() == ["a"]
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine_external.handle_event("AtoS2")
    assert statemachine_external.active_states() == ["s", "s2"]
    assert sequence == ["a:exit", "s:enter", "s2:enter"]

    sequence.clear()
    statemachine_external.handle_event("S2toT1")
    assert statemachine_external.active_states() == ["t", "t1"]
    assert sequence == ["s2:exit", "s:exit", "t:enter", "t1:enter"]

    sequence.clear()
    statemachine_external.handle_event("T1toS1")
    assert statemachine_external.active_states() == ["s", "s1"]
    assert sequence == ["t1:exit", "t:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine_external.handle_event("StoA")
    assert statemachine_external.active_states() == ["a"]
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine_external.teardown()
    assert statemachine_external.active_states() == []
    assert sequence == ["a:exit"]
