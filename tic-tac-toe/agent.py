# Immutable data structures
from pyrsistent import PClass, field

# Functional behavior
from phi import Pipe, Then, Then2, Then3

# For random decisions
import random as rand

import board, board_move, rewards
from board import X, O
from board_move import State as Move

EPSILON = 0.2 # Make random decision this much of the time
ALPHA = 0.99  # Discount future decisions by this factor

class State(PClass):
    """Agent state"""
    identifier = field()         # X or O
    epsilon = field()            # Probability of greedy vs. random decision
    alpha = field()              # Discount factor of future decisions
    learning = field()           # Whether to perform backup step
    rewards_state = field()      # Reward state
    last_board_state = field()   # Last board state

def player(identifier, rewards_state):
    """Non-learning agent that always makes greedy decision"""
    return State(
        identifier = identifier,
        epsilon = 0,
        alpha = ALPHA,
        learning = False,
        rewards_state = rewards_state,
        last_board_state = board.empty())

def learner(identifier, rewards_state):
    """Learning agent that makes trade-off between greedy/random decisions"""
    return player(identifier, rewards_state).set(
        learning = True,
        epsilon = EPSILON)

def move(state, board_state):
    """Agent move based on its policy (either greedy or random)"""
    if rand.random() < state.epsilon:
        # Make a random move (exploration)
        return _random_move(state, board_state)
    else:
        # Make a move based on known rewards (exploitation)
        return _greedy_move(state, board_state)

def reward_matrix(state, board_state):
    """Matrix of the reward value of all available moves"""

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
    """Perform backup when training epoch finishes"""
    rewards_state = state.rewards_state
    agent_id = state.identifier

    # Get reward based on final game state
    reward = rewards.lookupR(rewards_state, board_state, agent_id)

    # Update from last known board state (i.e. this agent's last move)
    rewards.backupR(rewards_state, state.last_board_state,
                    reward, agent_id, state.alpha)

def _random_move(state, board_state):
    """Choose a random move from the available ones"""
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
    """Helper function for returning move and updated agent state"""
    last_board_state = board.place(board_state, state.identifier, move)
    return (move, state.set(last_board_state = last_board_state))

def _reward_for_move(state, board_state, move):
    """Helper function for determining reward from suggested move"""
    return Pipe(
        # Create new board for looking up reward
        board.place(board_state, state.identifier, move),
        # Lookup reward (or default)
        Then2(rewards.lookupR, state.rewards_state, state.identifier))
