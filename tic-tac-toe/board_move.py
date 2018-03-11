# Immutable data structures
from pyrsistent import PClass, field

# Functional behavior
from phi import *

# Matrix transformations
import numpy as np

import board

class State(PClass):
    """Move state"""
    row = field()
    column = field()

# Point-free implementation of returning all available board moves
available = (
    F(board.available)
    >> np.where
    >> np.transpose
    >> list
    >> P.map(lambda x: State(row = x[0], column = x[1]))
)

