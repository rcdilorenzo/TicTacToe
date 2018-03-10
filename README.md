# Tic Tac Toe

[![demo](https://asciinema.org/a/168616.png)](https://asciinema.org/a/168616)

This repository contains a reinforcement learning algorithm wherein an agent is crafted with several default rewards (e.g. win, lose, and tie). It is trained by playing itself and then allowing the user to interact using a feature-rich CLI.

This 2-day project was inspired by the classic work by Sutton and Barton (2012) particularly the self-play discussion in exercise 1.1. I also referenced @tansey's [repository](https://github.com/tansey/rl-tictactoe/blob/master/tictactoe.py) for clarifying some details of a particular implementation.

## Installation

Assuming a package manager such as `pip`, the following dependencies are needed to run the CLI:

```bash
pip install urwid tabulate funcy phi pyrsistent numpy
```

To run, simply call `python tic-tac-toe` from within the directory.

## References

Sutton, R. S., & Barto, A. G. (2012). Reinforcement learning: an introduction (2nd ed.). Cambridge, MA: The MIT Press.
