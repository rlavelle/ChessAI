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


class RandomPlayer:

    def __init__(self, color:bool):
        self.color = color

    def makeMove(self, board):
        board.push(random.sample(list(board.legal_moves), 1)[0])

class CBRPlayer(AI):

    def __init__(self, player:bool, verbose=True, depth = 5):
        super().__init__(player, verbose)
        self.open_ai = OpenAI()
        self.use_open = True
        self.depth = depth

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
            while k < self.depth:
                self.count = 0
                self.pruned = 0
                self.dynamicProgramming = 0
                
                start = time.time()

                best_move, score = self.alpha_beta_minimax(board=board,
                                                           depth=k,
                                                           alpha=-math.inf,
                                                           beta=math.inf)
                end = time.time()

                if self.verbose:
                    print(f'depth: {k}, runtime: {end-start}, states visited: {self.count}, pruned: {self.pruned}, DP hits: {self.dynamicProgramming}')
                    print(k, best_move, score)
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
            usefulMoves = pruneMoves(board)
            for move in moves:
                if usefulMoves is not None and (move.from_square in usefulMoves[0] or move.to_square in usefulMoves[1]):
                    # if depth == self.depth-1:
                    #     print(1, move)
                    board.push(move)
                    _,score = self.alpha_beta_minimax(board=board,
                                                depth=depth-1,
                                                alpha=alpha,
                                                beta=beta)
                    board.pop()
                    if depth == self.depth-1:
                        print(move, score)
                    if score > best_score:
                        best_score, best_move = score, move

                    alpha = max(alpha,score)
                    if alpha >= beta: break
                elif usefulMoves is None:
                    # if depth == self.depth-1:
                    #     print(2, move)
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
                    # if depth == self.depth-1:
                    #     print(3, move)
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

# running pure alphabeta; no openAI or threat pruning 
class BasePlayer(AI):

    def __init__(self, player:bool, verbose=True, depth = 5, time_limit = 300, iterative = True):
        super().__init__(player, verbose)
        self.depth = depth
        self.iterative = iterative
        self.time_limit = time_limit
        
    def makeMove(self, board:Board):
        # IDS version of alpha beta

        k = 1
        start_hard = time.time()
        if self.iterative:
            while k < self.depth:
                self.count = 0
                self.dynamicProgramming = 0
                
                start = time.time()
                # break the program if it crosses the limit
                # TODO: implement the k-iterative within alpha-beta. 
                if abs(time.time() - start_hard) > self.time_limit:
                    break

                best_move, score = self.alpha_beta_minimax(board=board,
                                                            depth=k,
                                                            alpha=-math.inf,
                                                            beta=math.inf)
                end = time.time()
                if self.verbose:
                    print(f'depth: {k}, runtime: {end-start}, states visited: {self.count}, DP hits: {self.dynamicProgramming}')

                k += 1
            return best_move,score
        else:
            self.count = 0
            self.dynamicProgramming = 0
            
            start = time.time()

            best_move, score = self.alpha_beta_minimax(board=board,
                                                        depth=self.depth,
                                                        alpha=-math.inf,
                                                        beta=math.inf)
            end = time.time()
            if self.verbose:
                print(f'depth: {self.depth}, runtime: {end-start}, states visited: {self.count}, DP hits: {self.dynamicProgramming}')

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
                oldBoard = board.copy()
                board.push(move)
                _,score = self.alpha_beta_minimax(board=board,
                                            depth=depth-1,
                                            alpha=alpha,
                                            beta=beta)
                board.pop()
                if depth == self.depth-1:
                    print(move, score)
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
    board = chess.Board(fen='3r1k2/1pQ5/2B2pp1/p7/2P1P3/2K2P2/PP6/7R w - - 1 38')
    print(board)

    cbr = BasePlayer(chess.WHITE, verbose=True)

    move,score = cbr.makeMove(board)
    print(move)
    print(score)