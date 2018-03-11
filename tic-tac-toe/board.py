# Immutable data structures
from pyrsistent import PClass, field

# Functional behavior
from funcy import any, join
from phi import Then, Pipe

# Matrix manipulation
import numpy as np

_EMPTY = ' '
X = 'X'
O = 'O'

class State(PClass):
    """Board state wrapper to maintain immutability"""
    value = field()  # mutable numpy matrix

def empty():
    """Basic empty board state of 9 positions"""
    return State(value = np.matrix([
        [_EMPTY, _EMPTY, _EMPTY],
        [_EMPTY, _EMPTY, _EMPTY],
        [_EMPTY, _EMPTY, _EMPTY]
    ], dtype = 'S6'))

def not_id(identifier):
    """Returns opposite of current mark"""
    if identifier == X:   return O
    elif identifier == O: return X
    else:                 return _EMPTY

def at(state, index):
    """Helper function for getting mark using a flat array index"""
    return state.value[index / 3, index % 3]

def hash_key(state):
    """Compact representation of board for rewards"""
    return join(map(str, list(state.value.flat)))

def available(state):
    """Finds all empty positions in the board"""
    return state.value == _EMPTY

def is_empty(state):
    """Determines if all board positions are empty"""
    return Pipe(state, available, np.all)

def is_finished(state):
    """Determines if the game should be finished at this point"""
    return np.all(state.value != _EMPTY) or any_win(state)

def is_win(state, identifier):
    """Determines whether this identifier has won"""
    return any(Then(_is_slice_win, identifier), _win_slices(state))

def any_win(state):
    """Faster implementation for checking if any winning combinations exist"""
    return any(_is_slice_a_win, _win_slices(state))

def place(state, identifier, move):
    """Immutably places an identifier at a position on the board"""
    matrix = np.copy(state.value)

    # Check that move is available
    if matrix[move.row, move.column] == _EMPTY:
        matrix[move.row, move.column] = identifier

    return state.set(value = matrix)

def _win_slices(state):
    """Slices of the board state for checking if player has won"""
    matrix = state.value
    return [matrix[:, 0], matrix[:, 1], matrix[:, 2],   # Rows
            matrix[0, :], matrix[1, :], matrix[2, :],   # Columns
            np.diag(matrix), np.diag(np.rot90(matrix))] # Diagonals

def _is_slice_a_win(state_slice):
    """Checks if all marks are the same"""
    compacted = set(state_slice.flat)
    first = compacted.pop()

    # Verify contains only one unique element X or O
    return len(compacted) == 0 and (first == X or first == O)

def _is_slice_win(state_slice, identifier):
    """Checks if slice consists only of `identifier`"""
    return set(state_slice.flat) == set(identifier)

