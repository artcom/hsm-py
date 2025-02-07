import pytest

from hsm import State, Sub
from hsm import Statemachine


@pytest.fixture(name="sequence")
def sequence_fixture():
    yield []


@pytest.fixture(name="statemachine")
def statemachine_fixture(sequence):

    s1 = State("s1")
    s2 = State("s2")
    s = Sub('s', Statemachine(s1, s2))

    sm = Statemachine(s)

    def s_internal(data):
        sequence.append("s:internal")
    s.add_handler("internal", s, s_internal)

    def s1_internal(data):
        sequence.append("s1:internal")
    s1.add_handler("internal", s1, s1_internal)

    def s2_internal(data):
        sequence.append("s2:internal")
    s2.add_handler("internal", s2, s2_internal)

    s1.add_handler("leave", s2)
    s2.add_handler("leave", s1)

    def s_enter(data):
        sequence.append("s:enter")

    def s_exit(data):
        sequence.append("s:exit")

    def s1_enter(data):
        sequence.append("s1:enter")

    def s1_exit(data):
        sequence.append("s1:exit")

    def s2_enter(data):
        sequence.append("s2:enter")

    def s2_exit(data):
        sequence.append("s2:exit")

    s.enter_func = s_enter
    s.exit_func = s_exit
    s1.enter_func = s1_enter
    s1.exit_func = s1_exit
    s2.enter_func = s2_enter
    s2.exit_func = s2_exit

    sm.setup()
    yield sm


def test_event_bubbling(statemachine, sequence):

    sequence.clear()
    statemachine.handle_event("internal")
    assert sequence == ["s1:internal"]

    sequence.clear()
    statemachine.handle_event("leave")
    assert sequence == ["s1:exit", "s2:enter"]
