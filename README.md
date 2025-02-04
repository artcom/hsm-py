# HSM for Python

A hierarchical state machine implemented in Python

## Features

- simple states
- nested states (sub)
- least common ancestor algorithm
- run to completion

## System requirements

- Python 3.x.x

## Usage

```py
from hsm import State
from hsm import Statemachine

# Create the state hierarchy

a = State("a")

s1 = State("s1")
s2 = State("s2")
s = Sub('s', Statemachine(s1, s2))

sm = Statemachine(a, s)

# Enter and exit functions

def a_enter(data):
    # your code

def a_exit(data):
    # your code

a.enter_func = a_enter
a.exit_func = a_exit

# Define external transitions

a.add_handler("AtoS", s)
s1.add_handler("S1toS2", s2)
s2.add_handler("backToA", a)

# Define internal transitions

def a_internal(data):
    # your code

a.add_handler("Ainternal", a, a_internal)

# Starting the statemachine

sm.setup()

# Handling events

sm.handle_event("AtoS")
sm.handle_event("AtoS", { "something": 123 })

# Stopping the statemachine

sm.teardown()
```

For more examples see thte unit tests in `tests/*.py`

## Development

To run unit tests:

    python -m pytest tests
