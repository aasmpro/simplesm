from simplesm import SimpleSM


class TestMachine(SimpleSM):
    start_state = "S0"
    logic = {
        "S0": {"acceptable": False, "transitions": {
            "0": {"state": "S1", "event": "print"},
            "1": {"state": "S2"}
        }},
        "S1": {"acceptable": False, "transitions": {
            "1": {"state": "S0"}
        }},
        "S2": {"acceptable": True, "transitions": {
            "0": {"state": "S1", "event": "print"},
            "is_a_to_d": {"state": "S0"}
        }}
    }

    def print(self, action):
        print("going from {0} with {1}".format(self.current_state, action))

    def is_a_to_d(self, action):
        if action in "abcd":
            return True
        return False


def main():
    m = TestMachine()
    m.perform(list("011011a1nd011b0"))
    print(m.current_state)


if __name__ == '__main__':
    main()
