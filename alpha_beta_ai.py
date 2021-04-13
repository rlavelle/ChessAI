import chess
from functions import *
import copy
import math
import time

MAX_DEPTH = 6

class AI:
    def __init__(self,player, verbose):
        self.player = player
        self.verbose = verbose
        self.player_win_score = 10e10
        self.player_lose_score = -10e10
    
    def heuristic(self,board):
        return 0

    def heuristicZ(self, board):
        values = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 9
        }
        material = 0
        for pieceType in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
            material += len(board.pieces(pieceType, self.player))*values[pieceType]
            material -= len(board.pieces(pieceType, not self.player))*values[pieceType]
        return material * len(tuple(board.legal_moves))


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

            if self.verbose:
                print(f'depth: {k}, runtime: {end-start}, states visited {self.count}')

            k += 1
        return best_move,score

    def alpha_beta_minimax(self,board,depth,alpha,beta):
        self.count += 1
        terminal = board.outcome()

        # base cases (bottom of the minimax tree)
        if terminal:
            if terminal.winner == self.player:
                return None, self.player_win_score
            if terminal != self.player:
                return None, self.player_lose_score
        if depth == 0:
            return None, self.heuristic(board)
        
        # recursive case
        best_move = None
        
        moves = list(board.legal_moves)

        # maximize
        if board.turn == self.player:
            best_score = -math.inf
            for move in moves:
                board.push(move)
                _,score = self.alpha_beta_minimax(board=board,
                                                  depth=depth-1,
                                                  alpha=alpha,
                                                  beta=beta)
                board.pop()
                if score > best_score:
                    best_score, best_move = score, move

                alpha = max(alpha,score)
                if alpha >= beta: break
        # minimize
        else:
            best_score = math.inf
            for move in moves:
                board.push(move)
                _,score = self.alpha_beta_minimax(board=board,
                                                  depth=depth-1,
                                                  alpha=alpha,
                                                  beta=beta)
                board.pop()
                if score < best_score:
                    best_score, best_move = score, move

                beta = min(beta,score)
                if alpha >= beta: break 
        
        return best_move, best_score


if __name__ == "__main__":
    ai = AI(player=chess.WHITE)

    start_board = chess.Board()

    best_move, best_score = ai.get_best_move(board=start_board)

    print(best_move)

    start_board.push(best_move)
    print(start_board)