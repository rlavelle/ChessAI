from players import RandomPlayer, CBRPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
import sys
import chess
import numpy as np
np.random.seed(47)

# {'material': 1, 'positioning': 0.02, 'threat': 0.05}

def tournament(n):
    # generate n/2 random white/black players with random weights
    whites = [gen_players(chess.WHITE) for _ in range(n//2)]
    blacks = [gen_players(chess.BLACK) for _ in range(n//2)]

    # have each white player play each black player
    matches = []
    for white in whites:
        for black in blacks:
            matches.append((white,black))
    
    # play all matches out and collect winners
    winners = []
    for i,(white,black) in enumerate(matches):
        print(f'match {i}/{len(matches)}')
        winners.append(play_game(white,black))
    
    print(f'black winners: {len([w for w in winners if w.player == chess.BLACK])}')
    print(f'white winners: {len([w for w in winners if w.player == chess.WHITE])}')

# generate player of given color
def gen_players(color):
    # random weight between 0 and 10
    material_weight = np.random.random()*10

    # random number between 0 and 1 (since pst is large)
    position_weight = np.random.random()

    # number between 0 and 5 (threat is bigger than material)
    threat_weight = np.random.random()*5

    weights = {'material': material_weight, 
               'positioning': position_weight,
               'threat': threat_weight}

    return BasePlayer(player=color, depth=5, weights=weights)


def play_game(white:AI, black:AI, verbose = False):
    board = chess.Board()

    if verbose:
        print(board)
        print()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            board.push(white.makeMove(board)[0])
        elif board.turn == chess.BLACK:
            board.push(black.makeMove(board)[0])
        
        if verbose:
            print(board)
            print()
    
    terminal = board.outcome()
    
    if verbose:
        print("Game Over")
        print(f"Winner: {terminal.winner}")

    if terminal.winner == chess.WHITE:
        return white
    return black

    
if __name__ == "__main__":
    tournament(10)
