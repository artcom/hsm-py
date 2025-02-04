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


# pa = a.path()

# for e in pa:
#     print(e.name)
# print("-----")

# ps = s.path()

# for e in ps:
#     print(e.name)
# print("-----")

# psb = sb.path()

# for e in psb:
#     print(e.name)
# print("-----")


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
