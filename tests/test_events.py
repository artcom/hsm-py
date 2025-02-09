import pytest

from hsm import State, Sub, Statemachine, TransitionKind


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine_event_bubbling")
def statemachine_event_bubbling_fixture(sequence):
    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))
    sm = Statemachine(s)

    def s_internal(_):
        sequence.append("s:internal")
    s.add_handler("internal", s, s_internal, TransitionKind.INTERNAL)

    def s1_internal(_):
        sequence.append("s1:internal")
    s1.add_handler("internal", s1, s1_internal, TransitionKind.INTERNAL)

    def s2_internal(_):
        sequence.append("s2:internal")
    s2.add_handler("internal", s2, s2_internal, TransitionKind.INTERNAL)

    s1.add_handler("leave", s2)
    s2.add_handler("leave", s1)

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

    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    s2.enter_func = s2_enter
    s2.exit_func = s2_exit

    sm.setup()
    yield sm


@pytest.fixture(name="statemachine_event_queue")
def statemachine_event_queue_fixture(sequence):
    a = State("a")
    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))
    sm = Statemachine(a, s)

    a.add_handler("AtoA", a)
    a.add_handler("AtoS", s)
    s2.add_handler("S2toS2", s2)
    s1.add_handler("S1toS2", s2)

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

    a.enter_func = a_enter
    a.exit_func = a_exit
    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    s2.enter_func = s2_enter
    s2.exit_func = s2_exit

    sm.setup()
    yield sm


def test_event_bubbling(statemachine_event_bubbling, sequence):
    sequence.clear()
    statemachine_event_bubbling.handle_event("internal")
    assert sequence == ["s1:internal"]

    sequence.clear()
    statemachine_event_bubbling.handle_event("leave")
    assert sequence == ["s1:exit", "s2:enter"]


def test_event_queue(statemachine_event_queue, sequence):
    sequence.clear()
    statemachine_event_queue.handle_event("Ainternal")
    statemachine_event_queue.handle_event("AtoA")
    statemachine_event_queue.handle_event("AtoS")
    statemachine_event_queue.handle_event("S1toS2")
    statemachine_event_queue.handle_event("S2toS2")

    assert sequence == ["a:internal", "a:exit", "a:enter", "a:exit",
                        "s:enter", "s1:enter", "s1:exit", "s2:enter", "s2:exit", "s2:enter"]
