from pyrsistent import PClass, field, m
import board

class State(PClass):
    value = field() # Dictionary of board states to rewards

def empty():
    return State(value = m())

def curriedLookupR(state):
    return lambda b, i: lookupR(state, b, i)

def lookupR(state, board_state, identifier):
    return state.value.get(
        # Create short key from board
        board.hash(board_state),
        # Default to inherent rewards
        _value(board_state, identifier)
    )

# @mutable
def curriedBackupR(state):
    return lambda p, r, a: backupR(state, p, r, a)

# @mutable
def backupR(state, prev_board, reward, alpha):
    if board.is_empty(prev_board) == False:
        key = board.hash(prev_board)
        state[key] += alpha * (reward - state[key])

def _value(board_state, identifier):
    finished = board.is_finished(board_state)
    if finished == False:
        # Basic actions start as rewardless
        return 0
    elif board.is_win(board_state, identifier):
        # Winning has a high reward
        return 1.0
    else:
        # Draw is worth more than losing
        return 0.5
