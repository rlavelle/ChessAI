# Player classes
# Zach Wilkerson, Rowan Lavelle, Josep Han

from board import Board
import random
import chess
from pruning import *
from alpha_beta_ai import AI
import time
import math
from opening import OpenAI

MAX_DEPTH = 5

class RandomPlayer:

    def __init__(self, color:bool):
        self.color = color

    def makeMove(self, board):
        board.push(random.sample(list(board.legal_moves), 1)[0])

class CBRPlayer(AI):

    def __init__(self, player:bool, verbose=True):
        super().__init__(player, verbose)
        self.open_ai = OpenAI()
        self.use_open = True

    def makeMove(self, board:Board):
        # IDS version of alpha beta

        san_move = None

        if self.use_open:
            san_move, opening = self.open_ai.get_best_move(board)
        
        if san_move:
            best_move = board.parse_san(san_move)
            score = 0

            if self.verbose:
                print(f'playing {opening}')

            return best_move,score
        else:
            self.use_open = False
            
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
            return None, self.heuristic(board)
        
        # recursive case
        best_move = None
        
        moves = list(board.legal_moves)
        usefulMoves = pruneMoves(board)

        # maximize
        if board.turn == self.player:
            best_score = -math.inf
            for move in moves:
                if usefulMoves is not None and (move.from_square in usefulMoves[0] or move.to_square in usefulMoves[1]):
                    if depth == MAX_DEPTH-1:
                        print(1, move)
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
                elif usefulMoves is None:
                    if depth == MAX_DEPTH-1:
                        print(2, move)
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
                    if depth == MAX_DEPTH-1:
                        print(3, move)
                    self.pruned += 1
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