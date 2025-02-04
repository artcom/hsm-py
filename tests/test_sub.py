import pytest

from hsm.state import State, Sub
from hsm.statemachine import Statemachine


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):
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
    t.add_handler("TtoA", a)
    s1.add_handler("S1toS2", s2)
    s2.add_handler("S2toS1", s1)
    s1.add_handler("S1toT2", t2)
    s2.add_handler("S2toT1", t1)
    t1.add_handler("T1toS1", s1)

    def a_enter():
        sequence.append("a:enter")

    def a_exit():
        sequence.append("a:exit")

    def s_enter():
        sequence.append("s:enter")

    def s_exit():
        sequence.append("s:exit")

    def s1_enter():
        sequence.append("s1:enter")

    def s1_exit():
        sequence.append("s1:exit")

    def s2_enter():
        sequence.append("s2:enter")

    def s2_exit():
        sequence.append("s2:exit")

    def t_enter():
        sequence.append("t:enter")

    def t_exit():
        sequence.append("t:exit")

    def t1_enter():
        sequence.append("t1:enter")

    def t1_exit():
        sequence.append("t1:exit")

    def t2_enter():
        sequence.append("t2:enter")

    def t2_exit():
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


def test_sub_switching(statemachine, sequence):
    assert statemachine.current_state.name == "a"
    assert sequence == ["a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoA")
    assert statemachine.current_state.name == "a"
    assert sequence == ["a:exit", "a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoS")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s1"
    assert sequence == ["a:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("S1toS2")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s2"
    assert sequence == ["s1:exit", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toS2")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s2"
    assert sequence == ["s2:exit", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toS1")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s1"
    assert sequence == ["s2:exit", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("StoA")
    assert statemachine.current_state.name == "a"
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine.handle_event("AtoS2")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s2"
    assert sequence == ["a:exit", "s:enter", "s2:enter"]

    sequence.clear()
    statemachine.handle_event("S2toT1")
    assert statemachine.current_state.name == "t"
    assert statemachine.current_state.statemachine.current_state.name == "t1"
    assert sequence == ["s2:exit", "s:exit", "t:enter", "t1:enter"]

    sequence.clear()
    statemachine.handle_event("T1toS1")
    assert statemachine.current_state.name == "s"
    assert statemachine.current_state.statemachine.current_state.name == "s1"
    assert sequence == ["t1:exit", "t:exit", "s:enter", "s1:enter"]

    sequence.clear()
    statemachine.handle_event("StoA")
    assert statemachine.current_state.name == "a"
    assert sequence == ["s1:exit", "s:exit", "a:enter"]

    sequence.clear()
    statemachine.teardown()
    assert statemachine.current_state is None
    assert sequence == ["a:exit"]
