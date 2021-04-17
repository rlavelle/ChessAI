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
    chess.QUEEN : 9,
    chess.KING : 100000
}

# class PruningCase(Case):

#     def __init__(self, output = None):
#         super().__init__(output)

#     #NOTE: in this function, otherCase is actually a Board object for querying
#     def getDifference(self, otherCase):
#         differences = {}
#         for featureName in self.features.keys():
#             differences[featureName] = self.features[featureName].similarity(otherCase)
#         return differences


# class PruningCaseBase(CaseBase):

#     def __init__(self):
#         super().__init__()
#         threatCase = PruningCase()
#         threatCase.addFeature(Feature(None, "threat", threat))
#         self.addCase(threatCase)

#     def getPruning(self, query):
#         finalPruning = [False,chess.SquareSet()]
#         for caseHash in self.cases.keys():
#             prunings = self.getCase(caseHash).getDifference(query)
#             for featureName in prunings.keys():
#                 if prunings[featureName][0] is not None:
#                     finalPruning[0] = True
#                     for square in prunings[featureName][0]:
#                         finalPruning[1].add(square)
#                 else:
#                     if not finalPruning:
#                         for square in prunings[featureName][0]:
#                             finalPruning[1].add(square)
#         return finalPruning

"""
Initial plan = cases and adaptations, retrieved in a rule-based way
New plan = hierarchy of condition/response rules to determine possible prunings
"""

#==================================
# Condition Rules (tier 1)
#==================================

def threatenedPieces(board:chess.Board):
    threatenedPieces = chess.SquareSet()
    for pieceType in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
        for square in board.pieces(pieceType, board.turn):
            if board.is_attacked_by(not board.turn, square):
                threatenedPieces.add(square)
            # attackers = board.attackers(not board.turn, square)
            # for attackingSquare in attackers:
            #     if materialValue[board.piece_type_at(attackingSquare)] < materialValue[board.piece_type_at(square)]:
            #         threatenedPieces.add(square)
            #         break
    return threatenedPieces

def piecesThreatened(board:chess.Board):
    piecesThreatened = chess.SquareSet()
    for pieceType in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
        for square in board.pieces(pieceType, not board.turn):
            if board.is_attacked_by(board.turn, square):
                piecesThreatened.add(square)
    return piecesThreatened

#==================================
# Response Rules (tier 2)
#==================================

def threatResponse(board:chess.Board, threatenedPieces, piecesThreatened, validMoves_from_to = (chess.SquareSet(), chess.SquareSet())):
    for square in threatenedPieces:
        attackers = board.attackers(not board.turn, square)
        attackerStrength = []
        lowMaterialAttacker = False
        for attackingSquare in attackers:
            if materialValue[board.piece_type_at(attackingSquare)] < materialValue[board.piece_type_at(square)]:
                validMoves_from_to[0].add(square)
                lowMaterialAttacker = True
            if attackingSquare in piecesThreatened:
                validMoves_from_to[1].add(attackingSquare)
            if not lowMaterialAttacker:
                attackerStrength.append(materialValue[board.piece_type_at(attackingSquare)])
                attackerStrength.sort()
        if not lowMaterialAttacker:
            defenders = board.attackers(board.turn, square)
            if len(defenders) == 0:
                validMoves_from_to[0].add(square)
                continue
            defenderStrength = []
            for defendingSquare in defenders:
                defenderStrength.append(materialValue[board.piece_type_at(defendingSquare)])
                defenderStrength.sort()
            index = 0
            attackerStats = [0,0]
            defenderStats = [0,0]
            while True:
                try:
                    attackerStats[0] += attackerStrength[index]
                    attackerStats[1] += 1
                except:
                    attackerStats = attackerStats
                try:
                    defenderStats[0] += defenderStrength[index]
                    defenderStats[1] += 1
                except:
                    defenderStats = defenderStats
                if attackerStats[1] == defenderStats[1]:
                    if attackerStats[0] < defenderStats[0]:
                        validMoves_from_to[0].add(square)
                        break
                    elif attackerStats[0] > defenderStats[0]:
                        break
                    else:
                        if index == len(attackerStats):
                            break
                        else:
                            index += 1
                elif  attackerStats[1] > defenderStats[1]:
                    validMoves_from_to[0].add(square)
                    break
                else:
                    break
    return validMoves_from_to

def canThreatenResponse(board:chess.Board, piecesThreatened, validMoves_from_to = (chess.SquareSet(), chess.SquareSet())):
    for square in piecesThreatened:
        if len(validMoves_from_to[0]) == 0:
            validMoves_from_to[1].add(square)
    return validMoves_from_to

#TODO: this is the key function - need to balance pruning while not over-pruning
def genericResponse(proposedBoard:chess.Board, originalBoard:chess.Board, move:chess.Move):
    newPossibilities = proposedBoard.attacks(move.to_square)
    oldPossibilities = originalBoard.attacks(move.from_square)
    if len(newPossibilities) > len(oldPossibilities):
        return True
    else:
        reachableSquares = [0,0]
        for s in range(64):
            if proposedBoard.is_attacked_by(originalBoard.turn, s):
                reachableSquares[0] += 1
            if originalBoard.is_attacked_by(originalBoard.turn, s):
                reachableSquares[1] += 1
        if reachableSquares[0] > reachableSquares[1]:
            return True

        # oldDefenders = 0
        # newDefenders = 0
        # oldAttackers = 0
        # newAttackers = 0
        # for pieceType in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        #     for square in proposedBoard.pieces(pieceType, originalBoard.turn):
        #         oldDefenders += len(originalBoard.attackers(originalBoard.turn, square))
        #         newDefenders += len(proposedBoard.attackers(originalBoard.turn, square))
        #     for square in proposedBoard.pieces(pieceType, not originalBoard.turn):
        #         oldAttackers += len(originalBoard.attackers(originalBoard.turn, square))
        #         newAttackers += len(proposedBoard.attackers(originalBoard.turn, square))
        # if newDefenders > oldDefenders or newAttackers > oldAttackers:
        #     return True
    return False

    """
    Ideas:
    - If a piece is threatened
        - if attacker value is less, consider for moving
        - if another piece can capture the piece, consider the capture
        - if undefended, consider moving
    - If no obvious threats, prune pieces based on the following; moves should:
        - defend a piece
        - attack an opponent's piece (that is undefended or has less value)
        - make the piece more active (more attacking squares)
        - maximize overall number of attacked squares (?)
    """

def threatMoves(board:chess.Board):
    tP = threatenedPieces(board)
    pT = piecesThreatened(board)
    return canThreatenResponse(board, pT, threatResponse(board, tP, pT))