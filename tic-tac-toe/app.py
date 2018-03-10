from pyrsistent import PClass, field
from funcy import join, autocurry
from board import X, O
import time
import interface
import agent
import board
import rewards

EPOCHS = 15000
REWARDS = 'rewards'

class State:
    def __init__(self, rewards_state, agent_state, board_state):
        self.rewards_state = rewards_state
        self.agent_state = agent_state
        self.board_state = board_state
        self.ui = {}

def setup():
    return interface.setup(EPOCHS)

def run(loop, ui):
    rewards_state = _train(loop, ui)
    play_game(loop, rewards_state)

# @mutates
def play_game(loop, rewards_state):
    state = State(rewards_state, agent.player(X, rewards_state), board.empty())

    move_selected = autocurry(_move_selected)(state)
    interface.setup_game_play(loop, state, move_selected)

# @mutates
def _train(loop, ui):
    rewards_x = rewards.empty()

    for _ in range(0, EPOCHS):
        # Create agents to train against each other
        player1 = agent.learner(O, rewards.empty())
        player2 = agent.learner(X, rewards_x)

        # Play game
        result = _play_training_game(player1, player2)

        # Increment progress
        interface.train_epoch_finished(loop, ui)

    # Log to tsv file
    rewards.log(rewards_x)

    return rewards_x

# @mutates
def _move_selected(state, button, move):
    if button.get_label() in [X, O]:
        return interface.set_invalid_move_state(state)

    human_id = board.not_id(state.agent_state.identifier)
    state.board_state = board.place(state.board_state, human_id, move)
    interface.update_board(state)

    if board.is_finished(state.board_state):
        interface.game_finished(state)
    else:
        (move, agent_state) = agent.move(state.agent_state, state.board_state)
        state.board_state = board.place(
            state.board_state,
            state.agent_state.identifier,
            move)
        state.agent_state = agent_state
        interface.update_board(state)

    if board.is_finished(state.board_state):
        interface.game_finished(state)

# @mutates
def _play_training_game(player1, player2):
    # Initialize empty board
    board_state = board.empty()

    while board.is_finished(board_state) == False:
        # Player 1 turn
        (board_state, player1) = _play_train_move(player1, board_state)

        # Break if game already finished
        if board.is_finished(board_state): break

        # Player 2 turn
        (board_state, player2) = _play_train_move(player2, board_state)

    # Update rewards for final step
    agent.epoch_finished(player1, board_state)
    agent.epoch_finished(player2, board_state)

    # Return game winner
    return _winner(board_state, player1, player2)

# @mutates
def _play_train_move(player, board_state):
    (move, player) = agent.move(player, board_state)
    board_state = board.place(board_state, player.identifier, move)
    return (board_state, player)

def _winner(board_state, player1, player2):
    if board.is_win(board_state, player1.identifier):
        return player1
    elif board.is_win(board_state, player2.identifier):
        return player2
    else:
        return None
