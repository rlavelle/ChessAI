from board import Board
from functions import *
from pieces import *
import copy
import math
import time

MAX_DEPTH = 5

class AI:
    def __init__(self,turn):
        self.turn = turn
        self.player_win_score = 10e10
        self.player_lose_score = -10e10
    
    def heuristic(self,board):
        return 0

    def get_best_move(self,board):
        # IDS version of alpha beta
        k = 1
        while k < MAX_DEPTH:
            self.count = 0
            start = time.time()
            best_move, score = self.alpha_beta_minimax(board=board,
                                                       depth=k,
                                                       alpha=-math.inf,
                                                       beta=math.inf)
            end = time.time()
            k += 1

            print(f'depth: {k}, runtime: {end-start}, states visited {self.count}')
        return best_move,score

    def alpha_beta_minimax(self,board,depth,alpha,beta):
        self.count += 1
        terminal = board.isTerminal

        # base cases (bottom of the minimax tree)
        if terminal == 1:
            return None, self.player_win_score
        if terminal == 0:
            return None, self.player_lose_score
        if depth == 0:
            return None, self.heuristic(board)
        
        # recursive case
        best_move = None
        
        moves = board.successor()

        # maximize
        if board.turn == self.turn:
            best_score = -math.inf
            for move in moves:
                child_board = copy.deepcopy(board)
                child_board.makeMove(*move)

                _,score = self.alpha_beta_minimax(board=child_board,
                                                  depth=depth-1,
                                                  alpha=alpha,
                                                  beta=beta)
                if score > best_score:
                    best_score, best_move = score, move

                alpha = max(alpha,score)
                if alpha >= beta: break
        # minimize
        else:
            best_score = math.inf
            for move in moves:
                child_board = copy.deepcopy(board)
                child_board.makeMove(*move)

                _,score = self.alpha_beta_minimax(board=child_board,
                                                  depth=depth-1,
                                                  alpha=alpha,
                                                  beta=beta)
                if score < best_score:
                    best_score, best_move = score, move

                beta = min(beta,score)
                if alpha >= beta: break 
        
        return best_move, best_score


if __name__ == "__main__":
    ai = AI(turn=WHITE)

    start_board = Board(turn=WHITE)

    best_move, best_score = ai.get_best_move(board=start_board)

    print(best_move)

    start_board.makeMove(*best_move)
    print(start_board)