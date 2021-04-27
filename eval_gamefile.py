
import math
from players import BasePlayer
import chess
from chess import pgn
from chess import svg
from players import RandomPlayer, PruningPlayer
from alpha_beta_ai import AI
from opening import OpenAI
import time 
import math
import pickle
import numpy as np
import sys

def evaluate_gamefile(filename, eval_type = 'base',depth = 5, iterative = True):
    starttime = time.time()
    gamefile = open(filename)
    game = pgn.read_game(gamefile)
    # print('hi')
    # playing through a low rated game
    board = game.board()
    cbr = BasePlayer(chess.WHITE, verbose=True, depth = depth, iterative = iterative)
    if eval_type == 'rule':
        cbr = PruningPlayer(chess.WHITE, verbose = True, depth= depth+ 1)

    count = 1
    rec_moves = []
    moves = []
    board_configs = []
    time_taken = []
    # states_visited = []
    for move in game.mainline_moves():
        print(board.san(move))
        board_configs.append(board)
        board.push(move)
        damove = cbr.makeMove(board)
        print('\n',board,'\n',count, '\n',  damove)
        count+=0.5
        rec_moves.append(damove[0])
        if damove[1] > 1000:
            moves.append(25)
        if damove[1] < -1000:
            moves.append(-25)
        else:
            moves.append(damove[1])
        time_taken.append(abs(starttime - time.time()))
    print('average time taken per move: ' , np.mean(time_taken), 'total time:', time_taken[-1])
    return game, moves, board_configs, time_taken, rec_moves, time_taken[-1]


def save_game_eval(eval, filename):
    with open(filename, 'wb') as fp:
        pickle.dump(eval, fp, protocol = pickle.HIGHEST_PROTOCOL)

def load_eval(filename):
    with open(filename,'rb') as fp:
        loaded = pickle.load(fp)
    return loaded



if __name__ == '__main__': 
    if len(sys.argv) != 5:
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    filename  = sys.argv[1]
    depth     = sys.argv[2]
    eval_type = sys.argv[3]
    iterative = sys.argv[4]
    # evaluate_gamefile()
    # print(type(depth))
    # print(type(eval_type))
    # print(type(iterative))
    # print(type(depth))
    game = evaluate_gamefile(filename, eval_type=eval_type,depth=int(depth), iterative= iterative)
    savefile = str(filename) + str(depth) + str(eval_type) + str('.p')
    save_game_eval(game, savefile)

# low_game_base = evaluate_gamefile('lowgame1.pgn', depth = 4, iterative = False)
# mid_game_base = evaluate_gamefile('midgame.pgn', depth = 4, iterative = False)
# high_game_base = evaluate_gamefile('highgame.pgn',eval_type='rule', depth = 4, iterative = False)


