## simplesm
Simple state machine for python 3 that use dictionaries for creating states.

## Installation
```bash
pip3 install simplesm
```

## Documents
`SimpleSM` subclasses would have:

|Property|Description|
|--------|-----------|
|`start_state`|machine will start from this state.|
|`current_state`|machine current state|
|`previous_state`|machine previous state|
|`test_action`|test action shows current value to be tested, it will be set before testing it against machine states, so it will always have the latest value tested even if machine does not accept that action.|
|`current_action`|machine current action, this value will be set after action being accepted by state, so it will always have the latest acceptable value tested.|
|`previous_action`|just the last acceptable action before `current_action`.|
|`is_acceptable`|return `True` if machine is in a final state, otherwise `False`.|
|`states`|machine states! is a dict with keys as machine states, each state value is a dict too.|

Machine `states` dict values could have:

|Property|Description|
|--------|-----------|
|`transitions`|a dict that keys are acceptable actions (that could be string or a function name) and values are dicts with `state` that defines next state and `event` that defines event name to call.|
|`event`|this event will be called before testing action against machine states.|
|`else`|if none of `transitions` actions be accepted `else` will be called.|
|`final`|if exist and equals `True` shows that this state is a final state (means acceptable) otherwise state is not acceptable.|

Machine first tries to match action string against current state transitions, if not found one, then tries to call each current state transition and if it return `True` that transition will be accepted.

|Method|Description|
|--------|-----------|
|`perform(actions, do_events=True)`|get a string or list of strings as `actions` and try to perform that actions on machine, if `do_events` be `False`, `event`s will not be called.|
|`reset()`|set `current_state`, `previous_state`, `current_action`, `previous_action` and `test_action` to `None`.|
|`accept(self, actions, do_events=False)`|get a string or list of strings as `actions` and try to perform that actions on machine and return `True` if machine stops in a final state, otherwise `False`. this method does not change current values of machine and also by default does not call `event`s.|

## Usage and Features With [Example](simplesm/example.py)
Import `SimpleSM` from `simplesm` and create a class:
```python
from simplesm import SimpleSM


class TestMachine(SimpleSM):
    start_state = "S0"
    states = {
        "S0": {"transitions": {
            "0": {"state": "S1", "event": "print"},
            "1": {"state": "S2", "event": "print"}
        }, "event": "welcome"},
        "S1": {"final": False, "transitions": {
            "1": {"state": "S0", "event": "print"}
        }, "event": "welcome"},
        "S2": {"final": True, "transitions": {
            "0": {"state": "S1", "event": "print"},
            "2": {"state": "S3", "event": "print"},
            "is_a_to_d": {"state": "S0", "event": "print"}
        }, "else": "s2_wrong", "event": "welcome"},
        "S3": {"event": "goto_s2"}
    }

    def goto_s2(self):
        print("we are just going to state S2")
        self.current_state = "S2"

    def welcome(self):
        print("we are in state {0} and get action {1}".format(self.current_state, self.test_action))

    def print(self):
        print("going from {0} to {1} with {2}".format(self.previous_state, self.current_state, self.current_action))

    def s2_wrong(self):
        print("unacceptable input {0}".format(self.test_action))
        self.current_state = "Error"

    def is_a_to_d(self):
        if self.test_action in "abcd":
            return True
        return False


def main():
    m = TestMachine()
    m.perform(list("0110112a1d011"))
    print("current state is",m.current_state,"before calling accept")
    print("does machine accept 0110112a1d011 ?", m.accept(list("0110112a1d011")))
    print("current state is",m.current_state,"after calling accept")
    print("current state is acceptable ?", m.is_acceptable)


if __name__ == '__main__':
    main()
```

output:
```
we are in state S0 and get action 0
going from S0 to S1 with 0
we are in state S1 and get action 1
going from S1 to S0 with 1
we are in state S0 and get action 1
going from S0 to S2 with 1
we are in state S2 and get action 0
going from S2 to S1 with 0
we are in state S1 and get action 1
going from S1 to S0 with 1
we are in state S0 and get action 1
going from S0 to S2 with 1
we are in state S2 and get action 2
going from S2 to S3 with 2
we are just going to state S2
going from S2 to S0 with a
we are in state S0 and get action 1
going from S0 to S2 with 1
we are in state S2 and get action d
going from S2 to S0 with d
we are in state S0 and get action 0
going from S0 to S1 with 0
we are in state S1 and get action 1
going from S1 to S0 with 1
we are in state S0 and get action 1
going from S0 to S2 with 1
current state is S2 before calling accept
does machine accept 0110112a1d011 ? False
current state is S2 after calling accept
current state is acceptable ? True
```
