# Python Chess Game 

Run the player vs player file to play against another person

Run the player vs computer file to play against the given ai

Uses an mini-max alpha-beta pruning approach with a simple (to be updated) heuristic based on piece values

# Dependencies

Need to install the following with pip to be able to run files

- pygame, copy, subprocess

# TODOs

- Castling, En Passant
- Improvement of heuristic function, should take into account not only pieces value, but also its position on board (i.e knight should be more towards the center so they have more options for move)
- Fix endgame strategy for AI, weird bug where when i just have the white king on the board, the AI doesnt attack it until i bring the king closer to a piece (could be tree depth issue?)
# ChessAI
