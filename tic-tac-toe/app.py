import time
import interface

EPOCHS = 1000

def setup():
    (loop, ui) = interface.setup(EPOCHS)
    return (loop, ui, {})

def run(loop, ui, state):
    train(loop, ui, state)

def train(loop, ui, state):
    for i in range(0, 1000):
        time.sleep(0.02)
        interface.train_cycle_finished(loop, ui)
