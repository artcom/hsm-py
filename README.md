# HSM for Python

A hierarchical state machine implemented in Python

## Features

- simple states
- nested states (Sub)
- orthogonal regions (Parallel)
- external, internal and local transitions
- guard conditions
- least common ancestor algorithm
- run to completion model

## System requirements

- Python 3.11.x

## Usage

```py
from hsm import State
from hsm import Statemachine
from hsm import Sub
from hsm import Parallel

# Create the state hierarchy

a = State("a")

s1 = State("s1")
s2 = State("s2")
s = Sub('s', Statemachine(s1, s2))
p = Parallel('p', Statemachine(p1, p2), Statemachine(p3, p4))

sm = Statemachine(a, s, p)

# Enter and exit functions

def a_enter(data):
    # your code here

def a_exit(data):
    # your code here

a.enter_func = a_enter
a.exit_func = a_exit

# Define external transitions

a.add_handler("AtoS", s)
s1.add_handler("S1toS2", s2)
s2.add_handler("BackToA", a)

# Define internal transitions

from hsm import TransitionKind

def a_internal(data):
    # your code here

a.add_handler("Ainternal", a, action=a_internal, kind=TransitionKind.INTERNAL)

# Define local transitions

s.add_handler("Stos2", s2, kind=TransitionKind.LOCAL)

# Define guard conditions

def my_guard(data):
    return foo not in bar

a.add_handler("AtoS", s, guard=my_guard)

# Starting the statemachine

sm.setup()

# Handling events

sm.handle_event("AtoS")

# Passing data with event
# Data will be available in enter, exit functions and actions of internal transitions

sm.handle_event("AtoS", { "something": 123 })

# Stopping the statemachine

sm.teardown()
```

For more examples see the unit tests in `tests/*.py`

## Development

To install dev dependencies:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
pip install -r requirements_dev.txt
```

To run unit tests:

```sh
$ python -m pytest tests
```
