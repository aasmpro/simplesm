class SimpleSM:
    """simple state machine, based on python dicts.
    machine states are defined by states property. each state is a dict that can contain following values:
        final: bool >> defined if this state is final state
        event: str >> show which method should be called if machine is in that state
        transitions: dict >> each key shows an action str or method name which if input action equals to or the method
            called by the action returns True, that transition will be accepted. each transition value is a dict with
            these values:
                state: str >> show the next state to set
                event: str >> method name to be called after transition
        else: str >> a method name that if none of transitions be accepted, will be called.

    example:
    states = {'S0': {'final': False, 'event': 'method_a',
                     'transitions': {
                                    '0': {'state': 'S1', 'event': 'tr0_event'},
                                    '1': {'state': 'S2', 'event': 'tr1_event'}
                                    },
                     'else': 'method_of_else'
                    },
              'S1': {'transitions': {'method_01': {'state': 'S2'}},
              'S2': {'final': True}
              }
    """
    start_state = None
    current_state = None
    previous_state = None
    current_action = None
    previous_action = None
    test_action = None
    states = {}

    def perform(self, actions, do_events=True):
        """performing sequence of actions on state machine.
        each state event will be called before checking for transitions and transition event will be called after being
        accepted and machine state changed. in this events current_state, previous_state, current_action and
        previous_action properties are available.
        it first try to match action with transition, if none matched, it will try to call each transition as a method,
        where test_action property show the current action, so if method called return True, it will accept the action
        a change state of machine to what transition state say, otherwise if none of transitions work, try to call else
        method from state."""
        if not isinstance(actions, list) or isinstance(actions, tuple):
            actions = [actions]
        if not self.current_state:
            self.current_state = self.start_state
        for action in actions:
            self.test_action = action
            if do_events:
                try:
                    event = getattr(self, self.states[self.current_state]["event"])
                    event()
                except:
                    pass
            try:
                transition = self.states[self.current_state]["transitions"][action]
                self.previous_state = self.current_state
                self.current_state = transition["state"]
                self.previous_action = self.current_action
                self.current_action = action
                if do_events:
                    try:
                        event = getattr(self, transition["event"])
                        event()
                    except:
                        pass
            except:
                no_transition = True
                try:
                    for key, value in self.states[self.current_state]["transitions"].items():
                        try:
                            event = getattr(self, key)
                            result = event()
                            if result:
                                self.previous_state = self.current_state
                                self.current_state = value["state"]
                                self.previous_action = self.current_action
                                self.current_action = action
                                no_transition = False
                                if do_events:
                                    try:
                                        event = getattr(self, value["event"])
                                        event()
                                    except:
                                        pass
                                break
                        except:
                            pass
                except:
                    pass
                if no_transition:
                    try:
                        event = getattr(self, self.states[self.current_state]["else"])
                        event()
                    except:
                        pass

    def reset(self):
        """reset machine dynamic data to defaults."""
        self.current_state = None
        self.previous_state = None
        self.current_action = None
        self.previous_action = None
        self.test_action = None

    @property
    def is_acceptable(self):
        """has True value if the current state of machine has a final: True property, otherwise False."""
        try:
            return self.states[self.current_state]["final"]
        except:
            return False

    def accept(self, actions, do_events=False):
        """return True if the last state of machine after performing actions has a final: True, otherwise False.
        this method will keep current data of machine safe."""
        temp_current_state = self.current_state
        temp_previous_state = self.previous_state
        temp_current_action = self.current_action
        temp_previous_action = self.previous_action
        temp_test_action = self.test_action
        self.current_state = self.start_state
        self.perform(actions, do_events=do_events)
        result = self.is_acceptable
        self.current_state = temp_current_state
        self.previous_state = temp_previous_state
        self.current_action = temp_current_action
        self.previous_action = temp_previous_action
        self.test_action = temp_test_action
        return result
