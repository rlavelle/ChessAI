import chess
from functions import *
import copy
import math
import time
from abc import ABC, abstractmethod

class AI(ABC):
    def __init__(self,player, verbose = False):
        self.player = player
        self.verbose = verbose
        self.player_win_score = 10e10
        self.player_lose_score = -10e10

    def heuristic(self, board):
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
        return material # * len(tuple(board.legal_moves))

    @abstractmethod
    def makeMove(self,board):
        pass

    @abstractmethod
    def alpha_beta_minimax(self,board,depth,alpha,beta):
        pass