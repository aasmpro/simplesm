"""simple state machine"""


class SimpleSM:
    start_state = ""
    current_state = None
    logic = {}

    def perform(self, actions):
        try:
            if not isinstance(actions, list) or isinstance(actions, tuple):
                actions = [actions]
            for action in actions:
                if not self.current_state:
                    self.current_state = self.logic.get(self.start_state)
                transition = self.current_state["transitions"].get(action)
                if transition:
                    try:
                        event = getattr(self, transition.get("event"))
                        event(action)
                    except:
                        pass
                    self.current_state = self.logic.get(transition.get("state"))
                else:
                    for key, value in self.current_state["transitions"].items():
                        try:
                            event = getattr(self, key)
                            result = event(action)
                            if result:
                                try:
                                    event = getattr(self, value.get("event"))
                                    event(action)
                                except:
                                    pass
                                self.current_state = self.logic.get(value.get("state"))
                                break
                        except:
                            pass
        except:
            pass
