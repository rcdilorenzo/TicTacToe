import time
from funcy import autocurry
import interface
import agent
import board
import rewards

EPOCHS = 10000

def setup():
    (loop, ui) = interface.setup(EPOCHS)
    return (loop, ui, {})

def run(loop, ui, state):
    train(loop, ui, state)

def train(loop, ui, state):
    # Setup shared rewards
    state = rewards.empty()

    # Curry functions to refer to shared rewards state
    lookupR = autocurry(rewards.lookupR)(state)
    backupR = autocurry(rewards.backupR)(state)

    for _ in range(0, EPOCHS):
        # Create agents to train against each other
        player1 = agent.learner(board.X, lookupR, backupR)
        player2 = agent.learner(board.O, lookupR, backupR)

        # Play game
        result = play_game(agent, player1, agent, player2)

        # Increment progress
        interface.train_cycle_finished(loop, ui)

    rewards.log(state)

# @mutable
def play_game(controller1, player1, controller2, player2):
    # Initialize empty board
    board_state = board.empty()

    while board.is_finished(board_state) == False:
        # Player 1 turn
        board_state = play(controller1, player1, board_state)

        # Break if game already finished
        if board.is_finished(board_state): break

        # Player 2 turn
        board_state = play(controller2, player2, board_state)

    # Return game winner
    return winner(board_state, player1, player2)

# @mutable
def play(controller, player, board_state):
    move = controller.move(player, board_state)
    return board.place(board_state, player.identifier, move)

def winner(board_state, player1, player2):
    if board.is_win(board_state, player1.identifier):
        return player1
    elif board.is_win(board_state, player2.identifier):
        return player2
    else:
        return None
    
