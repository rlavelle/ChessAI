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

"""
Initial plan = cases and adaptations, retrieved in a rule-based way
New plan = hierarchy of condition/response rules to determine possible prunings
"""

#Moves to be pruned
#   Moves that don't improve the activity of pieces (i.e., number of legal moves in future boards)
#   Moves that lead to an obvious capture
#   Moves that don't deal with a current threat

#Moves to be kept
#   Moves that create new threats (esp. if can win the exchange)
#   Moves that restrict opponent's pieces

def evaluateExchange(board:chess.Board, square:chess.Square, initialMaterial:int = 0):
    defenders = board.attackers(board.turn, square)
    attackers = board.attackers(not board.turn, square)
    if len(attackers) == 0:
        return initialMaterial
    elif len(defenders) == 0:
        return initialMaterial - materialValue[board.piece_at(square)]
    attackerStrength = []
    for attackingSquare in attackers:
        attackerStrength.append(materialValue[board.piece_type_at(attackingSquare)])
        attackerStrength.sort()
    defenderStrength = []
    for defendingSquare in defenders:
        defenderStrength.append(materialValue[board.piece_type_at(defendingSquare)])
        defenderStrength.sort()
    index = 0
    material = initialMaterial - materialValue[board.piece_at(square)]
    if material > 0:
        return material
    while True:
        if index < len(defenderStrength):
            material += attackerStrength[index]
            if material < 0:
                return material
        else:
            return material
        if index < len(attackerStrength):
            material -= defenderStrength[index]
            if material > 0:
                return material
        else:
            return material

def pruneMoves(board:chess.Board):
    prev = board.copy()
    usefulMoves = (chess.SquareSet(), chess.SquareSet())
    legalMoves = board.legal_moves
    for move in legalMoves:
        # Piece is threatened by an opposing piece
        if board.is_attacked_by(not board.color, move.from_square):
            usefulMoves[0].add(move.from_square)
        else:
            board.push(move)
            if len(board.legal_moves) > len(legalMoves) and evaluateExchange(board, move.to_square) >= 0:
                usefulMoves[1].add(move.to_square)
            elif prev.is_capture(move) and evaluateExchange(board, move.to_square, materialValue[prev.piece_at(move.to_square)]) >= 0:
                usefulMoves[1].add(move.to_square)
    if len(usefulMoves[0]) > 0 or len(usefulMoves[1]) > 0:
        return usefulMoves
    else:
        return None


"""
#==================================
# Condition Rules (tier 1)
#==================================

# Determine which pieces are threatened (require attention)
#   board = the chessboard object
#   returns: a chess.SquareSet of threatened pieces
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

# Determine which pieces are currently attacked by your pieces
#   board = the chessboard object
#   returns: a chess.SquareSet of threatened pieces
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

# Hierarchical rule response based on pieces threatened
#   board = the chessboard object
#   threatenedPieces = your pieces that are threatened
#   piecesThreatened = opponent's pieces that you threaten
#   validMoves_from_to = set of moves that should be considered (others should be pruned if not empty); organized
#       as a tuple of chess.SquareSet objects representing from_square and to_square objects
#   returns: moves that should be considered
def threatResponse(board:chess.Board, threatenedPieces, piecesThreatened, validMoves_from_to = (chess.SquareSet(), chess.SquareSet())):
    for square in threatenedPieces:
        attackers = board.attackers(not board.turn, square)
        # attackerStrength = []
        for attackingSquare in attackers:
            # attacked by a piece worth less material (e.g., pawn attacks knight)
            # if materialValue[board.piece_type_at(attackingSquare)] < materialValue[board.piece_type_at(square)]:
            #     validMoves_from_to[0].add(square)
            validMoves_from_to[0].add(square)
            # if you can capture the attacker, consider the capture move
            if attackingSquare in piecesThreatened:
                validMoves_from_to[1].add(attackingSquare)
            # if not lowMaterialAttacker:
            #     attackerStrength.append(materialValue[board.piece_type_at(attackingSquare)])
            #     attackerStrength.sort()
        # determine whether you can afford an exchange
        # TODO: at this point, should we always consider it reasonable/possible to move the piece?
        # if not lowMaterialAttacker:
        #     defenders = board.attackers(board.turn, square)
        #     if len(defenders) == 0:
        #         validMoves_from_to[0].add(square)
        #         continue
        #     defenderStrength = []
        #     for defendingSquare in defenders:
        #         defenderStrength.append(materialValue[board.piece_type_at(defendingSquare)])
        #         defenderStrength.sort()
        #     index = 0
        #     attackerStats = [0,0]
        #     defenderStats = [0,0]
        #     while True:
        #         try:
        #             attackerStats[0] += attackerStrength[index]
        #             attackerStats[1] += 1
        #         except:
        #             attackerStats = attackerStats
        #         try:
        #             defenderStats[0] += defenderStrength[index]
        #             defenderStats[1] += 1
        #         except:
        #             defenderStats = defenderStats
        #         #same number of pieces attacking/defending (so far)
        #         if attackerStats[1] == defenderStats[1]:
        #             #attacker has smaller-material pieces attacking (can win the exchange)
        #             if attackerStats[0] < defenderStats[0]:
        #                 validMoves_from_to[0].add(square)
        #                 break
        #             # you can win the exchange
        #             elif attackerStats[0] > defenderStats[0]:
        #                 break
        #             # not yet decidable
        #             else:
        #                 if index == len(attackerStats):
        #                     break
        #                 else:
        #                     index += 1
        #         # opponent has more pieces attacking than you have defending
        #         elif  attackerStats[1] > defenderStats[1]:
        #             validMoves_from_to[0].add(square)
        #             break
        #         else:
        #             break
    return validMoves_from_to

# Hierarchical rule response based on offense
#   board = the chessboard object
#   piecesThreatened = opponent's pieces that you threaten
#   validMoves_from_to = set of moves that should be considered (others should be pruned if not empty); organized
#       as a tuple of chess.SquareSet objects representing from_square and to_square objects
#   returns: moves that should be considered
def canThreatenResponse(board:chess.Board, piecesThreatened, validMoves_from_to = (chess.SquareSet(), chess.SquareSet())):
    # for square in piecesThreatened:
    #     if len(validMoves_from_to[0]) == 0:
    #         validMoves_from_to[1].add(square)
    return validMoves_from_to

def positionalResponse(board:chess.Board, validMoves_from_to = (chess.SquareSet(), chess.SquareSet())):
    # prev = board.copy()
    # for move in board.legal_moves:
    #     board.push(move)
    #     if len(prev.attacks(move.from_square)) < len(board.attacks(move.to_square)):
    #         validMoves_from_to[0].add(move.from_square)
    #     # oldDefenders = 0
    #     # newDefenders = 0
    #     # for pieceType in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
    #     #         for square in board.pieces(pieceType, prev.turn):
    #     #             oldDefenders += len(prev.attackers(prev.turn, square))
    #     #             newDefenders += len(board.attackers(prev.turn, square))
    #     board.pop()
    if len(validMoves_from_to[0]) > 0 or len(validMoves_from_to[1]) > 0:
        return validMoves_from_to
    else:
        return None

#TODO: this is the key function - need to balance pruning while not over-pruning
# def genericResponse(proposedBoard:chess.Board, originalBoard:chess.Board, move:chess.Move):
#     newPossibilities = proposedBoard.attacks(move.to_square)
#     oldPossibilities = originalBoard.attacks(move.from_square)
#     if len(newPossibilities) > len(oldPossibilities):
#         return True
#     else:
#         reachableSquares = [0,0]
#         for s in range(64):
#             if proposedBoard.is_attacked_by(originalBoard.turn, s):
#                 reachableSquares[0] += 1
#             if originalBoard.is_attacked_by(originalBoard.turn, s):
#                 reachableSquares[1] += 1
#         if reachableSquares[0] > reachableSquares[1]:
#             return True

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
    # return False

# Wrapper function for these operations
#   board = the chessboard object
#   returns: the list of valid squares to consider
def pruneMoves(board:chess.Board):
    tP = threatenedPieces(board)
    pT = piecesThreatened(board)
    return positionalResponse(board, canThreatenResponse(board, pT, threatResponse(board, tP, pT, (chess.SquareSet(), chess.SquareSet()))))
"""