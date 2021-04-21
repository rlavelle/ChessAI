import chess
from functions import *
import copy
import math
import time
from abc import ABC, abstractmethod
import numpy as np 
class AI(ABC):
    def __init__(self,player, verbose = False):
        self.player = player
        self.verbose = verbose
        self.player_win_score = 10e10
        self.player_lose_score = -10e10

        # self.pawn_pst_white = (
        #     0,  0,  0,  0,  0,  0,  0,  0,
        #     50, 50, 50, 50, 50, 50, 50, 50,
        #     10, 10, 20, 30, 30, 20, 10, 10,
        #     5,  5, 10, 25, 25, 10,  5,  5,
        #     0,  0,  0, 20, 20,  0,  0,  0,
        #     5, -5,-10,  0,  0,-10, -5,  5,
        #     5, 10, 10,-20,-20, 10, 10,  5,
        #     0,  0,  0,  0,  0,  0,  0,  0
        # )
        # Converted the position tables as 1-d np arrays.
        self.pawn_pst_white = np.array([
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0]
        )
        self.pawn_pst_black = tuple(reversed(self.pawn_pst_white))

        self.knight_pst_white = np.array([
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50]
        )
        self.knight_pst_black = tuple(reversed(self.knight_pst_white))

        self.bishop_pst_white = np.array([
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20]
        )
        self.bishop_pst_black = tuple(reversed(self.bishop_pst_white))

        self.rook_pst_white = np.array([
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0]
        )
        self.rook_pst_black = tuple(reversed(self.rook_pst_white))

        self.queen_pst_white = np.array([
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20]
        )
        self.queen_pst_black = tuple(reversed(self.queen_pst_white))

        self.king_pst_white = np.array([
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20]
        )
        self.king_pst_black = tuple(reversed(self.king_pst_white))
        
        self.piece_square_table = {
            str(chess.PAWN)+str(chess.WHITE):self.pawn_pst_white,
            str(chess.PAWN)+str(chess.BLACK):self.pawn_pst_black,

            str(chess.KNIGHT)+str(chess.WHITE):self.knight_pst_white,
            str(chess.KNIGHT)+str(chess.BLACK):self.knight_pst_black,

            str(chess.BISHOP)+str(chess.WHITE):self.bishop_pst_white,
            str(chess.BISHOP)+str(chess.BLACK):self.bishop_pst_black,

            str(chess.ROOK)+str(chess.WHITE):self.rook_pst_white,
            str(chess.ROOK)+str(chess.BLACK):self.rook_pst_black,

            str(chess.QUEEN)+str(chess.WHITE):self.queen_pst_white,
            str(chess.QUEEN)+str(chess.BLACK):self.queen_pst_black,

            str(chess.KING)+str(chess.WHITE):self.king_pst_white,
            str(chess.KING)+str(chess.BLACK):self.king_pst_black,
        }

        self.material_value = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 9
        }

    """[Heuristic function for AI]
    multipart heuristic function to determine how good a given board is
        
        - material value: the value that each piece is assigned can help us determine
          if we have more "good" pieces than the opponent, or if they have more than us
       
        - piece positioning: using the piece-square tables we can assign value to a piece
          if its in a good location (board structure)
          reference: https://www.chessprogramming.org/Simplified_Evaluation_Function
        
        - mobility: using the board mobility we can see if our pieces are setup in a way
          that allows us to move, we penalize enemy mobility by taking the difference between
          our mobility and theirs. So a negative mobility means they can move more than we can
          TODO: do we care about this? 

        - threatening heuristic: we can value a board by looking at how many pieces our pieces are 
          in a position to capture (offense/defense)

        we assign each of these dimensions a weight the return the difference between
        white vs black. Negative values indicate a bad board for our AI, positive values
        indicate a good board for our AI, we can evalute the heuristic as such then
        
        white( ∑h_i*c_i ) - black( ∑h_i*c_i) where h_i and c_i denote the heuristics multiplied by
        their weights.
    """
    def heuristic(self, board):
        # weights for each heuristic
        weights = {'material': 1, 'positioning': 1, 'threat': 1}

        # find material value heuristic, and positioning heuristic
        material, positioning, threat = 0,0,0
        for pieceType in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
            # we care about the material of both us and opponent, so we take the difference
            material += len(board.pieces(pieceType, self.player))*self.material_value[pieceType]
            material -= len(board.pieces(pieceType, not self.player))*self.material_value[pieceType]
            
            for square in list(board.pieces(pieceType, self.player)):
                # we only care about the positioning of our pieces, this part is not a competition
                positioning += self.piece_square_table[str(pieceType)+str(self.player)][square]

                # pieces that being threatened by the enemy
                if board.is_attacked_by(not self.player, square):
                    threat -= 1
            
            for square in list(board.pieces(pieceType, not self.player)):
                # if we are threatening their piece
                if board.is_attacked_by(self.player, square):
                    threat += 1
        
        return material*weights['material'] + positioning*weights['positioning'] + threat*weights['threat']

    @abstractmethod
    def makeMove(self,board):
        pass

    @abstractmethod
    def alpha_beta_minimax(self,board,depth,alpha,beta):
        pass

class AITest(AI):
    def __init__(self,player,verbose=False):
        super().__init__(player, verbose)
    
    def makeMove(self,board):
        pass
    def alpha_beta_minimax(self,board,depth,alpha,beta):
        pass
if __name__ == "__main__":
    ai = AITest(chess.WHITE)
    print(ai.pawn_pst_good)
    print()
    print(ai.pawn_pst_bad)