from pyrsistent import PClass, field, m
from funcy import join
import board

class State(PClass):
    value = field() # Dictionary of board states to rewards

def empty():
    return State(value = dict())

# @mutates
def lookupR(state, board_state, identifier):
    return state.value.get(
        # Use board key
        board.hash_key(board_state),
        # Ensure default reward added
        _value(board_state, identifier))

# @mutates
def backupR(state, board_state, reward, identifier, alpha):
    if board.is_empty(board_state) == False:
        key = board.hash_key(board_state)

        # Perform classic RL backup reward update
        original = lookupR(state, board_state, identifier)
        state.value[key] = original + alpha * (reward - original)

def log(state):
    raw = state.value
    print(join(map(lambda k: k + ": " + str(raw[k]) + "\n", raw)))

def _value(board_state, identifier):
    finished = board.is_finished(board_state)
    if finished == False:
        # Basic actions start with no reward
        return 0
    elif board.is_win(board_state, identifier):
        # Winning has a high reward
        return 1.0
    else:
        # Draw is worth more than losing
        return 0.5
