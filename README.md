# Tic Tac Toe

![Sample CLI](https://user-images.githubusercontent.com/634167/37246650-6e7f1fbe-247b-11e8-92f1-fb071c02b223.png)

This repository contains a reinforcement learning algorithm wherein an agent is crafted with several default rewards (e.g. win, lose, and tie). It is trained by playing itself and then allowing the user to interact using a feature-rich CLI.

This 2-day project was inspired by the classic work by Sutton and Barton (2012) particularly the self-play discussion in exercise 1.1. I also referenced @tansey's [repository](https://github.com/tansey/rl-tictactoe/blob/master/tictactoe.py) for clarifying some details of a particular implementation.

## Installation

Assuming a package manager such as `pip`, the following dependencies are needed to run the CLI:

```bash
pip install urwid tabulate funcy phi pyrsistent numpy
```

To run, simply call `python tic-tac-toe` from within the directory.

## Demo Recording

<a href="https://asciinema.org/a/168616?t=1:05" target="_blank"><img src="https://asciinema.org/a/168616.png" width="50%" /></a>

## FAQ

1. Why does the "AI Brain" section seem to show the initial values?

Because the values are very close the original values, they appear to be the same. However, if you look at the actual values, they are different. This distinction is important for the AI as it currently chooses the highest reward for 

2. Where can I get the values that the algorithm produces?

When you run the project, a file is produced called `rewards.tsv` that includes the weights for the different scenarios encountered during the training process for the agent playing as the `X` mark.

## References

Sutton, R. S., & Barto, A. G. (2012). Reinforcement learning: an introduction (2nd ed.). Cambridge, MA: The MIT Press.
