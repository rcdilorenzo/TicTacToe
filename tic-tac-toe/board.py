from pyrsistent import PClass, field
from funcy import any, join
from phi import Then, Pipe
import numpy as np

_EMPTY = ' '
_WIN = np.matrix([[_EMPTY, _EMPTY, _EMPTY]])

X = 'X'
O = 'O'

class State(PClass):
    value = field() # numpy matrix

def empty():
    return State(value = np.matrix([
        [_EMPTY, _EMPTY, _EMPTY],
        [_EMPTY, _EMPTY, _EMPTY],
        [_EMPTY, _EMPTY, _EMPTY]
    ]))

def hash(state):
    return join(map(str, list(state.value.flat)))

def available(state):
    return state.value == _EMPTY

def is_empty(state):
    return Pipe(state, available, np.all)

def is_finished(state):
    return np.all(state.value != _EMPTY)

def is_win(state, identifier):
    matrix = state.value
    slices = [
        matrix[:, 0], matrix[:, 1], matrix[:, 2],
        matrix[0, :], matrix[1, :], matrix[2, :],
        np.diag(matrix), np.diag(np.rot90(matrix))
    ]
    return any(Then(_is_slice_win, identifier), slices)

def place(state, identifier, row, column):
    # Immutably update board state
    matrix = np.copy(state.value)
    if matrix[row, column] == _EMPTY:
        matrix[row, column] = identifier
    return state.set(value = matrix)

def _is_slice_win(state_slice, identifier):
    return list(set(state_slice.flat)) == [identifier]

