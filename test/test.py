from hsm.state import State, Sub
from hsm.statemachine import Statemachine

a = State("a")
sa = State("sa")
sb = State("sb")
s = Sub('s', Statemachine(sa, sb))

hsm = Statemachine(a, s)


a.add_handler("AtoS", s)
s.add_handler("StoA", a)

sa.add_handler("SAtoSB", sb)
sb.add_handler("SBtoSA", sa)

sa.add_handler("SAtoA", a)
sb.add_handler("SBtoA", a)
a.add_handler("AtoSB", sb)


def a_entry():
    print("enter a")


def a_exit():
    print("exit a")


def s_entry():
    print("enter s")


def s_exit():
    print("exit s")


def sa_entry():
    print("enter sa")


def sa_exit():
    print("exit sa")


def sb_entry():
    print("enter sb")


def sb_exit():
    print("exit sb")


a.enter_func = a_entry
a.exit_func = a_exit

s.enter_func = s_entry
s.exit_func = s_exit

sa.enter_func = sa_entry
sa.exit_func = sa_exit
sb.enter_func = sb_entry
sb.exit_func = sb_exit

hsm.setup()
print(".")


hsm.handle_event("AtoSB")
print(".")

hsm.handle_event("StoA")
print(".")
hsm.handle_event("SBtoSA")
print(".")
hsm.handle_event("SAtoSB")
print(".")

hsm.handle_event("SBtoA")
print(".")
