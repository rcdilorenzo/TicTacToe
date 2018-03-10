from pyrsistent import PClass, field
from funcy import autocurry
from board import X, O
import time
import interface
import agent
import board
import rewards

EPOCHS = 10000
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
    lookupR = autocurry(rewards.lookupR)(rewards_state)
    state = State(rewards_state, agent.player(X, lookupR), board.empty())

    move_selected = autocurry(_move_selected)(state)
    interface.setup_game_play(loop, state, move_selected)

def _train(loop, ui):
    # Setup shared rewards
    rewards_state = rewards.empty()

    # Curry functions to refer to shared rewards state
    lookupR = autocurry(rewards.lookupR)(rewards_state)
    backupR = autocurry(rewards.backupR)(rewards_state)

    for _ in range(0, EPOCHS):
        # Create agents to train against each other
        player1 = agent.learner(board.X, lookupR, backupR)
        player2 = agent.learner(board.O, lookupR, backupR)

        # Play game
        result = _play_training_game(agent, player1, agent, player2)

        # Increment progress
        interface.train_epoch_finished(loop, ui)

    # @mutates - log to tsv file
    rewards.log(rewards_state)

    return rewards_state

# @mutates
def _move_selected(state, button, move):
    if button.get_label() in [X, O]:
        return interface.set_invalid_move_state()

    state.board_state = board.place(state.board_state, O, move)
    interface.update_board(state)

    if board.is_finished(state.board_state):
        interface.game_finished(state)
    else:
        state.board_state = board.place(
            state.board_state,
            state.agent_state.identifier,
            agent.move(state.agent_state, state.board_state))
        interface.update_board(state)

    if board.is_finished(state.board_state):
        interface.game_finished(state)

# @mutates
def _play_training_game(controller1, player1, controller2, player2):
    # Initialize empty board
    board_state = board.empty()

    while board.is_finished(board_state) == False:
        # Player 1 turn
        board_state = _play(controller1, player1, board_state)

        # Break if game already finished
        if board.is_finished(board_state): break

        # Player 2 turn
        board_state = _play(controller2, player2, board_state)

    # Return game winner
    return _winner(board_state, player1, player2)

# @mutates
def _play(controller, player, board_state):
    move = controller.move(player, board_state)
    return board.place(board_state, player.identifier, move)

def _winner(board_state, player1, player2):
    if board.is_win(board_state, player1.identifier):
        return player1
    elif board.is_win(board_state, player2.identifier):
        return player2
    else:
        return None
