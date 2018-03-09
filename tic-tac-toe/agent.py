from pyrsistent import PClass, field, m
import board
from board import X, O

EPSILON = 0.1
ALPHA = 0.99

class State(PClass):
    identifier = field() # X or O
    backupR = field()    # Function for updating shared rewards state
    lookupR = field()    # Function for looking up shared rewards state
    epsilon = field()    # Probability of greedy vs. random decision
    alpha = field()      # Discount factor of future decisions

def player(identifier, lookupR):
    return State(
        identifier = identifier,
        backupR = lambda _s, _p, _r, _a: None,  # Do not update rewards
        lookupR = lookupR,
        epsilon = EPSILON,
        alpha = ALPHA
    )

def learner(identifier, lookupR, backupR):
    return player(identifier, lookupR).set(backupR = backupR)

def random(identifier, lookupR, backupR):
    return learner(identifier, lookupR, backupR).set(epsilon = 0)


