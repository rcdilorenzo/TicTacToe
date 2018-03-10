from pyrsistent import PClass, field
from phi import *
import numpy as np

import board

class State(PClass):
    row = field()
    column = field()

available = (
    F(board.available)
    >> np.where
    >> np.transpose
    >> list
    >> P.map(lambda x: State(row = x[0], column = x[1]))
)

