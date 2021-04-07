# Rule-based/case-based hybrid system for move pruning
# Zach Wilkerson

from cbr import Feature, Case, CaseBase
from board import Board
from functions import *

def analyze(board:Board):

    cases = []

    #==================================
    # Cases
    #==================================

    # If the king has castled, don't move any pawns in front of it
    if board.turn:
        kingPos = board.find_piece("K")
    else:
        kingPos = board.find_piece("K")
    kingPosXY = i_to_rc(kingPos)
    pruning = (kingPos) #TODO: create tuple of locations as the three spaces in front of the king's location (kingPos)
    castledKing = Case(pruning)
    for i in range(3):
        pass
    cases.append(castledKing)

    # If a piece is threatened by a pawn, that piece must be moved
    if board.turn:
        for piece in WHITE_PIECES:
            pieceLoc = board.find_piece(piece)
            # If threatened by a pawn, add a case with all other pieces removed/that piece highlighted
    else:
        for piece in BLACK_PIECES:
            pieceLoc = board.find_piece(piece)
            # Separate case, since the threat is two different diagonals

    # If a piece is pinned by a Bishop to a piece of greater value than that Bishop, don't move the piece
    if board.turn:
        for i in range(2):
            pieceLoc = board.find_piece("b",i)
            # See if Bishop can potentially threaten both the pinned piece and the more valuable piece
    else:
        for i in range(2):
            pieceLoc = board.find_piece("B",i)
            # Other color case

    # If the piece is pinned by a rook to a piece of greater value than that Rook, don't move the piece
            
    #==================================
    # Adaptations
    #==================================

    # OTHER IDEAS...?
    # Don't double pawns
    #
    # If the king has not yet moved (is in the center of the board), don't move it (unless castling)
    #
    # If a possible piece has something it can capture, make sure it has backup / is a fair trade
    #
    # if a Bishop/Queen/Rook has multiple open spaces that it can move, only consider spaces where it
    #       a) takes a piece
    #       b) is then in a position to capture a piece
    #       c) is then in a position to protect a piece
    # (this should hopefully eliminate checking moves where B/Q/R end up in empty space)
    # (maybe this will cut a branching factor of 8 down to 2/3 for pieces like this)