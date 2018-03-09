import time
import interface
import agent
import board
import rewards

EPOCHS = 1000

def setup():
    (loop, ui) = interface.setup(EPOCHS)
    return (loop, ui, {})

def run(loop, ui, state):
    train(loop, ui, state)

def train(loop, ui, state):
    for i in range(0, EPOCHS):
        # Setup shared rewards
        state = rewards.empty()
        lookupR = rewards.curriedLookupR(state)
        backupR = rewards.curriedBackupR(state)

        # Create agents to train against each other
        agent1 = agent.learner(board.X, lookupR, backupR)
        agent2 = agent.learner(board.O, lookupR, backupR)

        # TODO: Run training game
        # _training_game(rewards)
        interface.train_cycle_finished(loop, ui)

