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

def at(state, index):
    row = index / 3
    column = index % 3
    return state.value[row, column]

def hash_key(state):
    return join(map(str, list(state.value.flat)))

def available(state):
    return state.value == _EMPTY

def is_empty(state):
    return Pipe(state, available, np.all)

def is_finished(state):
    return np.all(state.value != _EMPTY) or any_win(state)

def is_win(state, identifier):
    return any(Then(_is_slice_win, identifier), _win_slices(state))

def any_win(state):
    return any(_is_slice_a_win, _win_slices(state))

def place(state, identifier, move):
    # Immutably update board state
    matrix = np.copy(state.value)
    if matrix[move.row, move.column] == _EMPTY:
        matrix[move.row, move.column] = identifier
    return state.set(value = matrix)

def _win_slices(state):
    matrix = state.value
    return [matrix[:, 0], matrix[:, 1], matrix[:, 2],
            matrix[0, :], matrix[1, :], matrix[2, :],
            np.diag(matrix), np.diag(np.rot90(matrix))]

def _is_slice_a_win(state_slice):
    compacted = set(state_slice.flat)
    first = compacted.pop()
    return len(compacted) == 0 and (first == X or first == O)

def _is_slice_win(state_slice, identifier):
    return list(set(state_slice.flat)) == [identifier]

