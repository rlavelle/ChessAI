from players import RandomPlayer, PruningPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
import chess
import time

def round_robin(players):
    # setup matches
    # have each player play each player
    matches = []
    for white in players:
        for black in players:
            if white == black: continue
            white.player = chess.WHITE
            black.player = chess.BLACK
            matches.append((white,black))
    
    wins = {p: 0 for p in players}
    
    # play all matches out and collect winners
    for i,(white,black) in enumerate(matches):
        # reset use_open to true, and reset the open AI
        white.use_open = True
        white.open_ai = OpenAI()
        black.use_open = True
        black.open_ai = OpenAI()
        
        print(f'match {i}/{len(matches)}')
        start = time.time()
        winner = play_game(white,black)
        end = time.time()
        print(f'game {i} took {(end-start)/60} min')
        wins[winner] += 1

    for winner in wins:
        print('AGENT')
        print(winner.weights)
        print(wins[winner])
        print()

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

def gen_players(w):
    return PruningPlayer(player=None, depth=5, verbose=False, weights=w)

if __name__ == "__main__":
    w1 = {'material': 9.752087678141946, 'positioning': 0.11126381956756781, 'threat': 3.5301550563650457}
    w2 = {'material': 1.1348847189364952, 'positioning': 0.3004364353612884, 'threat': 3.2042783890521287}
    w3 = {'material': 2.466493817746419, 'positioning': 0.3004364353612884, 'threat': 0.12005677072680465}
    w4 = {'material': 2.466493817746419, 'positioning': 0.9744830944364566, 'threat': 3.9980230083002692}
    w5 = {'material': 1.1348847189364952, 'positioning': 0.707605138259081, 'threat': 3.9980230083002692}
    w6 = {'material': 9.595035867576478, 'positioning': 0.707605138259081, 'threat': 3.9980230083002692}
    w7 = {'material': 2.466493817746419, 'positioning': 0.707605138259081, 'threat': 3.9980230083002692}
    base_w = {'material': 1, 'positioning': 0.02, 'threat': 0.05}
    weights = [w1,w2,w3,w4,w5,w6,w7,base_w]
    players = [gen_players(w) for w in weights]
    round_robin(players=players)
    #print(players)