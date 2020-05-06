"""
Class implementing mini-max with alpha-beta pruning to choose
the best next move given a current board

computer is always black in this case
"""

import math

TILE = 0
COLOR = 1
PIECE = 2

WHITE = (200, 255, 200)
BLACK = (130, 255, 130)


class AI:
    def __init__(self, depth, player):
        self.depth = depth
        self.player = player

    # calls the recursive alpha beta function with a given depth and starting values
    def make_best_move(self, board):
        score, move = self.alpha_beta(board, self.depth, self.player, -math.inf, math.inf)
        board.move(move[0], move[1])

    # returns best score and best move where a move is (from, to)
    def alpha_beta(self, board, depth, player, alpha, beta):
        # if we have reached depth or an end of board state
        if depth == 0 or board.terminal():
            return self.heuristic(board.board), -1

        # list of all children to a given board
        children = board.children(player)

        # if maximizing players turn
        if player:
            best_score = -math.inf
            best_move = -1
            # recur through all children to get best score
            for child in children:
                move, childboard = child
                score = self.alpha_beta(childboard, depth - 1, False, alpha, beta)[0]

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)

                # prune
                if beta <= alpha: break

            return best_score, best_move
        # if minimizing players turn
        else:
            best_score = math.inf
            best_move = -1
            # recur through all children to get best score
            for child in children:
                move, childboard = child
                score = self.alpha_beta(childboard, depth - 1, True, alpha, beta)[0]

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)

                # prune
                if beta <= alpha: break

            return best_score, best_move

    """
    returns a heuristic for a given board position
    good position for black pieces will give (+)
    good position for white pieces will give (-)
    
    heuristic is based on the following:
        -: a given piece's value
        -: how many piece's are on the board
        -: if you can put the king in check
        -: if pawns are poorly positioned  
    """
    def heuristic(self, board):
        h = 0

        # count all white and black pieces on board and P/B/Kn/R/Q
        # and check to see if you can take a piece or put king in check
        for tile in list(board.keys()):
            piece = board[tile][PIECE]
            if piece is not None:
                if piece.color == WHITE:
                    # whites pieces are valued higher than blacks to have our algorithm try and take pieces when it can
                    # aggressive strategy

                    # piece on board
                    h -= 5

                    # piece value
                    if piece.piece == " P ": h -= 200
                    if piece.piece == " B " or piece.piece == "Kn ": h -= 400
                    if piece.piece == " R ": h -= 600
                    if piece.piece == " Q ": h -= 800

                    # we get a board state where the white king is gone (capture white king)
                    if piece.piece == " K ": h -= 1500
                else:
                    # piece on board
                    h += 1

                    # piece value
                    if piece.piece == " P ": h += 10
                    if piece.piece == " B " or piece.piece == "Kn ": h += 30
                    if piece.piece == " R ": h += 50

                    # value of queen is larger than other pieces because we want to keep it on board as long as possible
                    if piece.piece == " Q ": h += 900

                    # we want to get a board where out black king is still alive (move out of check)
                    if piece.piece == " K ": h += 1500

                    # see if we can put king in check
                    for move in piece.get_moves(board):
                        if board[move][PIECE] is not None:
                            # there exists a move to put the white king in check (very good)
                            if board[move][PIECE].piece == " K " and board[move][PIECE].color == WHITE:
                                h += 10000

        # check if all black pawns are in the same first row (no channels to leave from the back) (bad)
        # we want to have pawns from B7, D7, E7, G7 move forward in the beginning to open knights, bishops, and queen
        for tile in list(board.keys()):
            piece = board[tile][PIECE]
            if piece is not None:
                if piece.color == BLACK:
                    if piece.piece == " P " and (piece.square == "B7" or piece.square == "D7" or piece.square == "E7" or piece.square == "G7"):
                        h -= 20
        return h
