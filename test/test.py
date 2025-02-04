from hsm.state import State, Sub
from hsm.statemachine import Statemachine

a = State("a")
s1 = State("s1")
s2 = State("s2")
s = Sub('s', Statemachine(s1, s2))

hsm = Statemachine(a, s)


a.add_handler("AtoS", s)
s.add_handler("StoA", a)

s1.add_handler("S1toS2", s2)
s2.add_handler("S2toS1", s1)

s1.add_handler("S1toA", a)
s2.add_handler("S2toA", a)
a.add_handler("AtoS2", s2)


def a_entry():
    print("enter a")


def a_exit():
    print("exit a")


def s_entry():
    print("enter s")


def s_exit():
    print("exit s")


def s1_entry():
    print("enter s1")


def s1_exit():
    print("exit s1")


def s2_entry():
    print("enter s2")


def s2_exit():
    print("exit s2")


a.enter_func = a_entry
a.exit_func = a_exit

s.enter_func = s_entry
s.exit_func = s_exit

s1.enter_func = s1_entry
s1.exit_func = s1_exit
s2.enter_func = s2_entry
s2.exit_func = s2_exit

hsm.setup()
print(".")


hsm.handle_event("AtoS2")
print(".")

hsm.handle_event("StoA")
print(".")
hsm.handle_event("S2toS1")
print(".")
hsm.handle_event("S1toS2")
print(".")

hsm.handle_event("S2toA")
print(".")
