from players import RandomPlayer, CBRPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
import chess

def gen_avg_opening_moves():
    n_games = 30
    cbr_open = []
    random_open = []
    base_open = []

    for i in range(n_games):
        print(f'game {i}')

        print(f'cbr playing...')
        # cbr opening move counting
        # our player
        player_a = CBRPlayer(chess.WHITE, verbose=False)
        player_b = CBRPlayer(chess.BLACK, verbose=False)
        cbr_open.append(play_game(player_a,player_b))

        print(f'random playing...')
        # random opening counter
        player_a = CBRPlayer(chess.WHITE, verbose=False)
        player_b = RandomPlayer(chess.BLACK)
        random_open.append(play_game(player_a,player_b))

        print(f'base player playing...')
        # base opening counter
        player_a = CBRPlayer(chess.WHITE, verbose=False)
        player_b = BasePlayer(chess.BLACK, verbose=False)
        base_open.append(play_game(player_a,player_b))

        print('', flush=True)
    
    return sum(cbr_open)/n_games, sum(random_open)/n_games, sum(base_open)/n_games

def play_game(white:AI, black:AI, verbose = False):
    moves = 0
    
    board = chess.Board()

    if verbose:
        print(board)
        print()
        
    while True:
        if board.turn == chess.WHITE:
            board.push(white.makeMove(board)[0])
            if white.use_open:
                moves += 1
            else:
                break
        elif board.turn == chess.BLACK:
            if type(black) == RandomPlayer:
                black.makeMove(board)
            else:
                board.push(black.makeMove(board)[0])
        
        if verbose:
            print(board)
            print()

    return moves


if __name__ == "__main__":
    avg_cbr, avg_random, avg_base = gen_avg_opening_moves()
    print(f'cbr v. cbr average number of opening moves {avg_cbr}')
    print(f'cbr v. random player average number of opening moves {avg_random}')
    print(f'cbr v. base player average number of opening moves {avg_base}')




