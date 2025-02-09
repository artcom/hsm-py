import pytest

from hsm import Parallel, State, Sub, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
    a = State("a")
    s1 = State("s1")
    s2 = State("s2")
    s = Sub("s", Statemachine(s1, s2))
    t1 = State("t1")
    t2 = State("t2")
    t = Sub("t", Statemachine(t1, t2))

    p11 = State("p11")
    p12 = State("p12")
    p21 = State("p21")
    p22 = State("p22")
    p = Parallel("p", Statemachine(p11, p12), Statemachine(p21, p22))
    sm = Statemachine(a, s, t, p)

    def a_internal(_):
        sequence.append("a:internal")

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

    def p_enter(_):
        sequence.append("p:enter")

    def p_exit(_):
        sequence.append("p:exit")

    def p11_enter(_):
        sequence.append("p11:enter")

    def p11_exit(_):
        sequence.append("p11:exit")

    def p12_enter(_):
        sequence.append("p12:enter")

    def p12_exit(_):
        sequence.append("p12:exit")

    def p21_enter(_):
        sequence.append("p21:enter")

    def p21_exit(_):
        sequence.append("p21:exit")

    def p22_enter(_):
        sequence.append("p22:enter")

    def p22_exit(_):
        sequence.append("p22:exit")

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

    p.enter_func = p_enter
    p.exit_func = p_exit
    p11.enter_func = p11_enter
    p11.exit_func = p11_exit
    p12.enter_func = p12_enter
    p12.exit_func = p12_exit
    p21.enter_func = p21_enter
    p21.exit_func = p21_exit
    p22.enter_func = p22_enter
    p22.exit_func = p22_exit

    a.add_handler("Ainternal", a, action=a_internal,
                  kind=TransitionKind.INTERNAL)

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

    a.add_handler("AtoP22", p22)
    p22.add_handler("P22toP21", p21)
    p21.add_handler("P21toP12", p12)

    sm.setup()
    yield sm


def test_external_transitions(statemachine, sequence):
    sequence.clear()
    statemachine.handle_event("AtoA")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["a:exit", "a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoS")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["a:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("S1toS")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["s1:exit", "s:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("S1toS2")
    assert statemachine.active_states() == ["s", "s2"]
    assert sequence == ["s1:exit", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toS2")
    assert statemachine.active_states() == ["s", "s2"]
    assert sequence == ["s2:exit", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toS1")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["s2:exit", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("StoA")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoS2")
    assert statemachine.active_states() == ["s", "s2"]
    assert sequence == ["a:exit", "s:enter", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toT1")
    assert statemachine.active_states() == ["t", "t1"]
    assert sequence == ["s2:exit", "s:exit", "t:enter", "t1:enter"]

    sequence.clear()
    statemachine.handle_event("T1toS1")
    assert statemachine.active_states() == ["s", "s1"]
    assert sequence == ["t1:exit", "t:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("StoA")
    assert statemachine.active_states() == ["a"]
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoP22")
    assert statemachine.active_states() == ["p", "p11", "p22"]
    assert sequence == ["a:exit", "p:enter", "p11:enter", "p22:enter"]

    sequence.clear()
    statemachine.handle_event("P22toP21")
    assert statemachine.active_states() == ["p", "p11", "p21"]
    assert sequence == ["p22:exit", "p21:enter"]

    sequence.clear()
    statemachine.handle_event("P21toP12")
    assert statemachine.active_states() == ["p", "p12", "p21"]
    assert sequence == ["p11:exit", "p21:exit",
                        "p:exit", "p:enter", "p12:enter", "p21:enter"]

    sequence.clear()
    statemachine.teardown()
    assert statemachine.active_states() == []
    assert sequence == ["p12:exit", "p21:exit", "p:exit"]
