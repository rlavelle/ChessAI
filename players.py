# Player classes
# Zach Wilkerson, Rowan Lavelle, Josep Han

from board import Board
import random
import chess
from pruning import PruningCaseBase
from alpha_beta_ai import AI
import time
import math

MAX_DEPTH = 5

class RandomPlayer:

    def __init__(self, color:bool):
        self.color = color
    
    # def makeMove(self, board:Board):
    #     possibleMoves = []
    #     for pieceLoc in board.piece_locs[self.color].keys():
    #         possibleMoves = possibleMoves + board.piece_locs[self.color][pieceLoc][1].getMoves(board)
    #     move = random.sample(possibleMoves, 1)[0]
    #     board.makeMove(tuple(move)[0], tuple(move)[1])

    def makeMove(self, board):
        board.push(random.sample(list(board.legal_moves), 1)[0])

class CBRPlayer(AI):

    def __init__(self, player:bool, verbose=True):
        super().__init__(player, verbose)
        self.cb = PruningCaseBase()

    def makeMove(self, board:Board):
        # IDS version of alpha beta
        k = 1
        while k < MAX_DEPTH:
            self.count = 0
            self.pruned = 0
            start = time.time()
            best_move, score = self.alpha_beta_minimax(board=board,
                                                       depth=k,
                                                       alpha=-math.inf,
                                                       beta=math.inf)
            end = time.time()

            if self.verbose:
                print(f'depth: {k}, runtime: {end-start}, states visited: {self.count}, pruned: {self.pruned}')

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
            return None, self.heuristicZ(board)
        
        # recursive case
        best_move = None
        
        moves = list(board.legal_moves)
        prunings = self.cb.getPruning(board)

        # maximize
        if board.turn == self.player:
            best_score = -math.inf
            if prunings[0]:
                for move in moves:
                    if len(prunings[1]) > 0 and move.from_square not in prunings[1]:
                        self.pruned += 1
                        continue
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
            else:
                for move in moves:
                    if len(prunings[1]) > 0 and move.from_square in prunings[1]:
                        self.pruned += 1
                        continue
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