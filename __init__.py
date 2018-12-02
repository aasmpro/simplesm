from .simplesm import SimpleSM

__title__ = 'simplesocket'
__version__ = '0.1.0'
__author__ = 'Abolfazl Amiri'
__author_email__ = 'aa.smpro@gmail.com'
__license__ = 'GNU General Public License v3 (GPLv3)'
__all__ = ['SimpleSM']
__description__ = """simplesm 0.1.0
simple state machine, based on python dicts.
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
