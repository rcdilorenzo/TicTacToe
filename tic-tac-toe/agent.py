from pyrsistent import PClass, field, m
from phi import Pipe, Then, Then3
import random as rand

import board, board_move
from board import X, O
from board_move import State as Move

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
        backupR = lambda _p, _r, _i, _a: None,  # Do not update rewards
        lookupR = lookupR,
        epsilon = EPSILON,
        alpha = ALPHA
    )

def learner(identifier, lookupR, backupR):
    return player(identifier, lookupR).set(backupR = backupR)

def random(identifier, lookupR, backupR):
    return learner(identifier, lookupR, backupR).set(epsilon = 0)

def move(state, board_state):
    if rand.random() < state.epsilon:
        return _random_move(state, board_state)
    else:
        return _greedy_move(state, board_state)

def _random_move(_state, board_state):
    return Pipe(board_state, board_move.available, rand.choice)

# @mutates
def _greedy_move(state, board_state):
    # Get available moves
    moves = board_move.available(board_state)

    # Get best move by reward
    move = max(moves, key = Then3(_reward_for_move, state, board_state))

    # Update rewards based on this move's reward
    reward = _reward_for_move(state, board_state, move)
    state.backupR(board_state, reward, state.identifier, state.alpha)

    # Return best move
    return move

def _reward_for_move(state, board_state, move):
    return Pipe(
        # Create new board for looking up reward
        board.place(board_state, state.identifier, move),
        # Lookup reward (or default)
        Then(state.lookupR, state.identifier))
