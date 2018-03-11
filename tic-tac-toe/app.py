# Immutable data structures
from pyrsistent import PClass, field

# Functional behavior
from funcy import join, autocurry

from board import X, O
import interface, agent, board, rewards

EPOCHS = 15000
REWARDS = 'rewards'

class State:
    """Mutable, top-level application state while in game play"""
    def __init__(self, rewards_state, agent_state, board_state):
        self.rewards_state = rewards_state
        self.agent_state = agent_state
        self.board_state = board_state
        self.ui = {}

def setup():
    """Basic app setup"""
    return interface.setup(EPOCHS)

def run(loop, ui):
    """App entry point, includes training and entering game play"""
    rewards_state = _train(loop, ui)
    play_game(loop, rewards_state)

# @mutates
def play_game(loop, rewards_state):
    """Setup game play state and interface"""

    # Initialize top-level, mutable state with agent X
    state = State(rewards_state, agent.player(X, rewards_state), board.empty())

    # Curry move_selected for referring to correct app state
    move_selected = autocurry(_move_selected)(state)

    # Setup game interface
    interface.setup_game_play(loop, state, move_selected)

# @mutates
def _train(loop, ui):
    """Training phase for two agents to learn by playing each other"""
    rewards_x = rewards.empty()

    # Train iteratively until rewards start to converge
    for _ in range(0, EPOCHS):
        # Create agents to train against each other
        player1 = agent.learner(O, rewards.empty())
        player2 = agent.learner(X, rewards_x)

        # Play game
        _play_training_game(player1, player2)

        # Increment progress
        interface.train_epoch_finished(loop, ui)

    # Log to tsv file
    rewards.log(rewards_x)

    # Return rewards for later access
    return rewards_x

# @mutates
def _move_selected(state, button, move):
    """Interface callback for proceeding through game play with user"""

    # Guard clause for when already-filled place is attempted
    if button.get_label() in [X, O]:
        return interface.set_invalid_move_state(state)

    # Update board state based on move
    human_id = board.not_id(state.agent_state.identifier)
    state.board_state = board.place(state.board_state, human_id, move)

    # Update UI to reflect model
    interface.update_board(state)

    # Check for game finished
    if board.is_finished(state.board_state):
        # Display game results
        interface.game_finished(state)
    else:
        # Process agent's decision
        (move, agent_state) = agent.move(state.agent_state, state.board_state)

        # Update board and agent state
        state.board_state = board.place(
            state.board_state,
            state.agent_state.identifier,
            move)
        state.agent_state = agent_state

        # Update UI to reflect model
        interface.update_board(state)

    # Another check for game finish to prevent inadvertent user events
    if board.is_finished(state.board_state):
        # Display game results
        interface.game_finished(state)

# @mutates
def _play_training_game(player1, player2):
    """Simulated game between two agents"""

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

# @mutates
def _play_train_move(player, board_state):
    """Helper for handling single agent's move"""

    # Get move and updated player state
    (move, player) = agent.move(player, board_state)

    # Update board state
    board_state = board.place(board_state, player.identifier, move)

    return (board_state, player)
