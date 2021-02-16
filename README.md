# Python Chess Game 

An interactive python chess game made using pygame. The AI uses the minimax algorithm along with the alpha-beta pruning optimization. As of right now the heuristic is very basic.

## requirements

Make sure you are using python3 and set up a virtual environment by running

```
python3 -m venv env
```

Then activate the environment

```
source env/bin/activate
```

Then go ahead and install the requirements

```
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## running the program

If you want to play against a friend, go into the src directory and run:

```
python3 player_vs_player.py
```

If you want to play against the AI run:

```
python3 player_vs_computer.py
```

## Optimizations and future improvements

### Game improvements

- Castling, En Passant
- make it so clicking on a piece can be unselected if you want to move another piece
- when clicking a piece, show all available moves 

### AI improvements
- Improvement of heuristic function, should take into account not only pieces value, but also its position on board (i.e knight should be more towards the center so they have more options for moves)
- Use professional chess game data to train a feed forward neural network to act as the heuristic

## data

Data for this project can be found at the following [here](https://www.ficsgames.org): matches are from 2008-2016

# Future of the project

In the future I want to write a version of this program that is only the AI file. Once I find a suitable javascript implementation of in-browser chess, from there I want to re-write the AI file to be wrapped in an API that can take in a board, and respond with a json file of the next move. This way the game can be added to [my website](https://www.rowanlavelle.com). Along with this, I think minimax / alpha-beta pruning can be optimized even further using dynamic programing and iterative deepening search (IDS) instead of just a singular depth limit, with IDS stopping at some request time limit.
