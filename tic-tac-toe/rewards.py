# Immutable data structures
from pyrsistent import PClass, field

# Functional behavior
from funcy import join

import board

class State(PClass):
    """Reward state (internally mutable)"""
    value = field() # Dictionary of board states to rewards

def empty():
    """Empty reward state"""
    return State(value = dict())

# @mutates
def lookupR(state, board_state, identifier):
    """Lookup current reward or use the default reward prescribed"""
    return state.value.get(
        # Use board key
        board.hash_key(board_state),
        # Use default reward otherwise
        _value(board_state, identifier))

# @mutates
def backupR(state, previous_board_state, reward, identifier, alpha):
    """Update reward based on V(s) += a[V(s') - V(s)]"""

    # Only update with non-empty board
    if board.is_empty(previous_board_state) == False:
        # Use compact board key
        key = board.hash_key(previous_board_state)

        # Perform classic backup reward update
        original = lookupR(state, previous_board_state, identifier)
        state.value[key] = original + alpha * (reward - original)

# @mutates
def log(state):
    """Log all rewards to tab-separated file"""
    raw = state.value
    result = join(map(lambda k: k + "\t" + str(raw[k]) + "\n", raw))
    with open('rewards.tsv', 'w') as f:
        f.write(result)

def _value(board_state, identifier):
    """Defines default rewards"""
    finished = board.is_finished(board_state)
    if finished == False:
        # Basic actions start with negative reward
        return -0.5
    elif board.is_win(board_state, identifier):
        # Winning has a high reward
        return 1.0
    elif board.is_win(board_state, board.not_id(identifier)):
        # Losing is a negative reward
        return -1.0
    else:
        # Draw is worth more than losing
        return 0.5
