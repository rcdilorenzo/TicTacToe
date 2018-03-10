from pyrsistent import PClass, field
from phi import Pipe, Then, Then2, Then3
import random as rand

import board, board_move, rewards
from board import X, O
from board_move import State as Move

EPSILON = 0.2
ALPHA = 0.99

class State(PClass):
    identifier = field()         # X or O
    epsilon = field()            # Probability of greedy vs. random decision
    alpha = field()              # Discount factor of future decisions
    learning = field()           # Whether to perform backup step
    rewards_state = field()      # Reward state
    last_board_state = field()   # Last board state

def player(identifier, rewards_state):
    return State(
        identifier = identifier,
        epsilon = 0,
        alpha = ALPHA,
        learning = False,
        rewards_state = rewards_state,
        last_board_state = board.empty()
    )

def learner(identifier, rewards_state):
    return player(identifier, rewards_state).set(
        learning = True,
        epsilon = EPSILON
    )

def move(state, board_state):
    if rand.random() < state.epsilon:
        return _random_move(state, board_state)
    else:
        return _greedy_move(state, board_state)

def reward_matrix(state, board_state):
    return reduce(
        # Accumulate board with reward for each move
        lambda acc, m: board.place(
            acc, "{0:.3f}".format(_reward_for_move(state, board_state, m)), m),
        # Get available moves
        board_move.available(board_state),
        # Use board as initial state
        board_state).value

# @mutates
def epoch_finished(state, board_state):
    rewards_state = state.rewards_state
    agent_id = state.identifier
    reward = rewards.lookupR(rewards_state, board_state, agent_id)
    rewards.backupR(rewards_state, state.last_board_state,
                    reward, agent_id, state.alpha)

def _random_move(state, board_state):
    return Pipe(
        # Get available moves
        board_move.available(board_state),
        # Choose one randomly
        rand.choice,
        # Return move and updated state
        Then3(_move_and_agent, state, board_state))

# @mutates
def _greedy_move(state, board_state):
    # Get available moves
    moves = board_move.available(board_state)

    # Get best move by reward
    move = max(moves, key = Then3(_reward_for_move, state, board_state))

    # @mutates - Update rewards based on this move's reward
    if state.learning:
        reward = _reward_for_move(state, board_state, move)
        rewards.backupR(
            state.rewards_state, state.last_board_state,
            reward, state.identifier, state.alpha)

    # Return best move
    return _move_and_agent(state, board_state, move)

def _move_and_agent(state, board_state, move):
    last_board_state = board.place(board_state, state.identifier, move)
    return (move, state.set(last_board_state = last_board_state))

def _reward_for_move(state, board_state, move):
    return Pipe(
        # Create new board for looking up reward
        board.place(board_state, state.identifier, move),
        # Lookup reward (or default)
        Then2(rewards.lookupR, state.rewards_state, state.identifier))
