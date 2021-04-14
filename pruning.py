# Rule-based/case-based hybrid system for move pruning
# Zach Wilkerson

from cbr import Feature, Case, CaseBase
from functions import *
from sys import maxsize
import chess

materialValue = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 9
        }

class PruningCase(Case):

    def __init__(self, output = None):
        super().__init__(output)

    #NOTE: in this function, otherCase is actually a Board object for querying
    def getDifference(self, otherCase):
        differences = {}
        for featureName in self.features.keys():
            differences[featureName] = self.features[featureName].similarity(otherCase)
        return differences


class PruningCaseBase(CaseBase):

    def __init__(self):
        super().__init__()
        threatCase = PruningCase()
        threatCase.addFeature(Feature(None, "threat", threat))
        self.addCase(threatCase)

    def getPruning(self, query):
        finalPruning = [False,chess.SquareSet()]
        for caseHash in self.cases.keys():
            prunings = self.getCase(caseHash).getDifference(query)
            for featureName in prunings.keys():
                if prunings[featureName][0] is not None:
                    finalPruning[0] = True
                    for square in prunings[featureName][0]:
                        finalPruning[1].add(square)
                else:
                    if not finalPruning:
                        for square in prunings[featureName][0]:
                            finalPruning[1].add(square)
        return finalPruning

#==================================
# Cases
#==================================

def threat(board:chess.Board):
    threatenedPieces = chess.SquareSet()
    for pieceType in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
        for square in board.pieces(pieceType, board.turn):
            attackers = board.attackers(not board.turn, square)
            for attackingSquare in attackers:
                try:
                    if materialValue[board.piece_at(attackingSquare).piece_type] < materialValue[board.piece_at(square).piece_type]:
                        threatenedPieces.add(square)
                        break
                except:
                    print(board.piece_at(attackingSquare).piece_type, board.piece_at(square).piece_type)
                    print(board.piece_at(attackingSquare), board.piece_at(square))
                    print(board)
                    print(attackingSquare, square)
    return (threatenedPieces, None)

#TODO: consider a moveablePieces field for board to avoid double-counting when applying CBR

#If a piece is pinned to a more valuable piece, do not move it
# def pinned(board:Board):
#     unconsideredPieces = []
#     for opposingPieceLoc in board.piece_locs[not board.turn].keys():
#         for potentialThreatenedPiece in board.piece_locs[board.turn].keys():
#             for potentialPinnedPiece in board.piece_locs[board.turn].keys():
#                 valuePieceDist = board.piece_locs[opposingPieceLoc][1].canThreaten(potentialThreatenedPiece[0], potentialThreatenedPiece[1])
#                 pinnedPieceDist = board.piece_locs[opposingPieceLoc][1].canThreaten(potentialPinnedPiece[0], potentialPinnedPiece[1])
#                 if valuePieceDist is None or pinnedPieceDist is None:
#                     continue
#                 else:
#                     if valuePieceDist[0]-pinnedPieceDist[0] >= 0 and valuePieceDist[1]-pinnedPieceDist[1] >= 0 and \
#                         board.piece_locs[potentialPinnedPiece][1].value < board.piece_locs[potentialThreatenedPiece][1].value:
#                         unconsideredPieces.append(potentialPinnedPiece)
#     return unconsideredPieces

            
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