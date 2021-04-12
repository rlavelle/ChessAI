# Player classes
# Zach Wilkerson, Rowan Lavelle, Josep Han

from board import Board
import random
import chess
from pruning import PruningCaseBase

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

class CBRPlayer:

    def __init__(self, color:bool):
        self.color = color
        self.cb = PruningCaseBase()

    def makeMoe(self, board:Board):
        pass