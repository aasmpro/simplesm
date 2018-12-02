from simplesm.simplesm import SimpleSM


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
        print("yes!")
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
    print(m.current_state)
    print(m.accept(list("0110112a1d011")))
    print(m.current_state)


if __name__ == '__main__':
    main()
